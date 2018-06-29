# coding:utf8
'''
author : Guoxi
email  : splinzer@gmail.com
time   : 2018/06/21 上午9:45
'''
from shutil import which


def which_app(namelist: list) -> dict:
    """which_app用于判断想要调用的程序是否可用
    根据所给的程序名称列表，返回当前系统可用的程序字典：键是程序名，值是路径
    :param namelist: 程序名称列表
    :return dict: 可用的程序名列表
    例如：
    which_app(['wget',
                    'curl',
                    'firefox',
                    'chromium-browser',
                    'explorer'])
    返回值为：   {'wget': '/usr/bin/wget',
                'curl': '/usr/bin/curl',
                'firefox': '/usr/bin/firefox',
                'chromium-browser': '/usr/bin/chromium-browser'}
    这说明系统上找不到名为explorer的程序
    """
    return {x: which(x) for x in namelist if which(x)}


from socket import socket
import struct
import json


class JsonTcp:
    """tcp打包类
    该类解决使用tcp进行通信的粘包问题，解决办法是构造固定长度的消息head+变长消息body，在消息head中记录消息body长度和消息类型编号，
    在接收时首先读取消息头，并根据消息body的长度获取消息body。

    - 服务端例子：

        from socket import socket
        import struct
        from ptcp import JsonTcp

        with socket() as s:
            s.bind((‘’, 1234))
            s.listen(1)
            conn, addr = s.accept()
            with conn:
                print(JsonTcp.recv_one(conn))

    - 客户端例子：

        from socket import socket
        from ptcp import JsonTcp

        client = socket()
        client.connect(('',1234))

        # 正常数据包定义
        sendData = JsonTcp.pack(body={'say':"hello world"}, cmd=101)
        client.send(sendData)

    """
    # 消息头格式定义
    fmt = '!I'
    # 计算消息头大小
    headerSize = struct.calcsize(fmt)
    bufferSize = 1024

    @classmethod
    def pack(cls, data=None, status: str = None, name: str = None) -> bytes:
        """tcp打包方法

        :param data: 消息体，可以是Python的基本数据类型
        :param status:状态
        :param name:
        :return: 以bytes形式返回打包后的数据
        """
        assert data, 'data参数不能为空'
        msg = {
            'status': status,
            'name': name,
            'data': data
        }
        msg = json.dumps(msg).encode()

        headPack = struct.pack(cls.fmt, len(msg))
        return headPack + msg

    @classmethod
    def recv_one(cls, sock: socket):
        """从指定socket只接收一个数据报
        :param sock: 套接字
        :return: 数据报，格式为 (body, sock)，如超时返回None
        """
        try:
            it = cls.recvfrom(sock, pack_num=1)
            return next(it)
        except StopIteration:
            return

    @classmethod
    def recvfrom(cls, sock: socket, pack_num=0):
        """从指定socket接收tcp数据并解包
        :param sock:套接字
        :param pack_num:想要获取的数据包个数，默认为0表示不限数量。当指定了大于0的数字之后，该方法在返回了指定数量的数据包后停止循环。
        :return:返回一个iterable对象 (body,sock)
        """

        dataBuffer = bytes()
        # 记录已获取的数据报个数
        n = 0
        while True:
            data = sock.recv(cls.bufferSize)
            headerSize = cls.headerSize
            if data:
                # 把数据存入缓冲区，类似于push数据
                dataBuffer += data
                while True:
                    # 当已经获取到了指定数量的数据报，且n不为默认值时，退出方法
                    if n == pack_num and n:
                        return
                    # 只有接收完头部才能继续
                    if len(dataBuffer) < headerSize:
                        # print("数据包（%s Byte）小于消息头部长度，跳出小循环" % len(dataBuffer))
                        break

                    # 读取包头
                    # struct中:!代表Network order，I代表2个unsigned int数据
                    headPack = struct.unpack(cls.fmt, dataBuffer[:headerSize])
                    bodySize = headPack[0]

                    # 分包情况处理，跳出函数继续接收数据
                    if len(dataBuffer) < headerSize + bodySize:
                        # print("数据包（%s Byte）不完整（总共%s Byte），跳出小循环" % (len(dataBuffer), headerSize+bodySize))
                        break
                    # 读取消息正文的内容
                    body = dataBuffer[headerSize:headerSize + bodySize]
                    body = json.loads(body)

                    # 粘包情况的处理
                    dataBuffer = dataBuffer[headerSize + bodySize:]  # 获取下一个数据包，类似于把数据pop出

                    # 调返回解析结果
                    yield (body, sock)
                    n += 1
            else:
                print('客户端断开', sock)
                sock.close()
                break
