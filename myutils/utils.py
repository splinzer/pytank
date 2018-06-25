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


class Ptcp:
    """tcp打包类
    该类解决使用tcp进行通信的粘包问题，解决办法是构造固定长度的消息head+变长消息body，在消息head中记录消息body长度和消息类型编号，
    在接收时首先读取消息头，并根据消息body的长度获取消息body。

    - 服务端例子：

        from socket import socket
        import struct
        from ptcp import Ptcp

        # 定义回调函数
        def callback(sock, head, body):
            print(head, body)

        with socket() as s:
            s.bind((‘’, 1234))
            s.listen(1)
            while True:
                conn, addr = s.accept()
                with conn:
                    Ptcp.unpack(conn, callback)

    - 客户端例子：

        from socket import socket
        from ptcp import Ptcp

        client = socket()
        client.connect(('',1234))

        # 正常数据包定义
        sendData = Ptcp.pack({'say':"hello world"}, 101)
        client.send(sendData)

    """
    fmt = '!2I'
    headerSize = struct.calcsize(fmt)

    @classmethod
    def pack(cls, body=None, cmd=1)-> bytes:
        """tcp打包方法

        :param body: 消息体，可以是Python的基本数据类型
        :param cmd: 整数，用于表示消息类型
        :return: 以bytes形式返回打包后的数据
        """
        assert type(cmd) is int, 'cmd参数必须为正整数'
        assert body, 'body参数不能为空'
        data = json.dumps(body).encode()
        header = [cmd, len(data)]
        headPack = struct.pack(cls.fmt, *header)
        return headPack + data

    @classmethod
    def unpack(cls, sock: socket, callback=None):
        """tcp解包方法
        param sock:套接字
        param callback:回调函数callback(sock, head, body)，接受3个参数head和body，当解包成功后自动调用
        """

        dataBuffer = bytes()

        while True:
            data = sock.recv(1024)
            headerSize = cls.headerSize
            if data:
                # 把数据存入缓冲区，类似于push数据
                dataBuffer += data
                while True:
                    # 只有接收完头部才能继续
                    if len(dataBuffer) < headerSize:
                        # print("数据包（%s Byte）小于消息头部长度，跳出小循环" % len(dataBuffer))
                        break

                    # 读取包头
                    # struct中:!代表Network order，2I代表2个unsigned int数据
                    headPack = struct.unpack('!2I', dataBuffer[:headerSize])
                    cmd = headPack[0]
                    bodySize = headPack[1]

                    # 分包情况处理，跳出函数继续接收数据
                    if len(dataBuffer) < headerSize + bodySize:
                        # print("数据包（%s Byte）不完整（总共%s Byte），跳出小循环" % (len(dataBuffer), headerSize+bodySize))
                        break
                    # 读取消息正文的内容
                    body = dataBuffer[headerSize:headerSize + bodySize]
                    body = json.loads(body)
                    # 调用回调函数返回解析结果
                    callback(sock, cmd, body)
                    # 粘包情况的处理
                    dataBuffer = dataBuffer[headerSize + bodySize:]  # 获取下一个数据包，类似于把数据pop出
            else:
                print('客户端断开', sock)
                sock.close()
                break
