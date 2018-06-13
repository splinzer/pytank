# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 下午7:47
from socket import *
from time import sleep
from multiprocessing import Process, Pipe, Queue
from importlib import import_module
from pathlib import Path
from client.clientcoder import Coder
import json
import zlib

# 战场更新频率
FRAMERATE = 0.05
# webscoket服务器host
HOST = ''
# socket服务端口
PORT = 9000
# webscoket服务器端口
WEBSOCKET_PORT = 8000
# 观战网页文件的本地地址
WEBSOCKET_CLIENT_URL = '/client/websocket.html'
# 坦克AI数量有效范围
ALLOW_COUNT = (2, 5)
# 缓冲区大小
BUFFER_SIZE = 2096


class Client:
    def __init__(self):
        # 战场id
        self.battle_id = None
        # 坦克id列表
        self.tank_id_list = []
        # 战场上所有坦克AI的输入数据队列
        self.in_queues = []
        # 战场上所有坦克AI的输出数据队列
        self.out_queues = []
        self.s = None
        self.connect()

    def game_over(self):
        pass

    def connect(self):
        self.s = socket(AF_INET, SOCK_DGRAM)
        self.s.connect((HOST, PORT))
        # 登录验证
        while True:
            # 导入坦克AI程序
            tank_count, self.tankAIs = self.load_tankais()
            # 检测坦克AI程序数量是否在有效范围内（ALLOW_COUNT）
            self.check_tankAIs(tank_count)
            # 尝试登录，并如能登录，则告知服务器创建tankcount个坦克的战场
            username, password = self.getverifyinfo()
            msg = 'LOGIN' + username + '|' + password + '|' + str(tank_count)
            self.s.send(msg.encode())
            # 服务器响应
            response = self.s.recv(BUFFER_SIZE).decode()
            # 响应内容格式：'ok|battle_id|tank_id1|tank_id2|...'
            response = response.split('|')
            if response[0] == 'ok':
                print('[client]登录成功')
                self.battle_id = response[1]
                self.tank_id_list = response[2:]
                # 初始化坦克AI进程
                self.init_tanks_process()
                break
            else:
                print('[client]登录失败')
                continue

        # 主循环
        while True:
            # 接收服务端战场信息
            data = self.s.recv(BUFFER_SIZE)

            # 判断游戏结束
            if data == b'gameover':
                # todo 显示游戏结果
                self.game_over()
                break

            # 使用前解压数据
            data = zlib.decompress(data)
            # print('[client]收到<战场数据>:', data)
            data = data.decode()
            # 将信息通过queue转发给各坦克AI和websocket
            for in_queue in self.in_queues:
                # 反序列化info
                in_queue.put(self.decodeinfo(data))

            # 获取各坦克的指令发给服务器
            # todo 目前各坦克的指令分别发出，考虑合并更高效
            for out_queue in self.out_queues:
                if not out_queue.empty():
                    action_str = out_queue.get()
                    self.send_to_server(action_str)
                else:
                    pass
                    # print('[client]暂无<指令>')
        os.wait()

    def send_to_server(self, action_str):
        # 使用json对指令进行序列化处理
        action_json = json.dumps(action_str)
        # print('[client]发出<指令>:', action_json)
        # 发给服务端
        self.s.send(action_json.encode())

    def check_tankAIs(self, tank_count):
        if ALLOW_COUNT[0] > tank_count > ALLOW_COUNT[1]:
            sys.exit(f'[client]警告<坦克AI数量必须在{ALLOW_COUNT}个内>')

    def init_tanks_process(self):
        """
        为每个坦克AI创建一个独立进程，每个进程拥有分别拥有输入数据和输出数据队列用来和主进程通讯
        :return:
        """
        print(f'[client]初始化<坦克AI进程>')
        n = 0
        for m in self.tankAIs:
            # todo 这里为每个tankAI使用了单独的in_queue和out_queue，可以考虑合并
            # 坦克控制逻辑的输入数据队列
            in_queue = Queue()
            self.in_queues.append(in_queue)
            # 坦克控制逻辑的输出数据队列
            out_queue = Queue()
            self.out_queues.append(out_queue)
            # 每个坦克控制逻辑对应一个进程
            p = Process(target=m.AI, args=(in_queue, out_queue, self.battle_id, self.tank_id_list[n]))
            p.start()
            n += 1

    def getverifyinfo(self):
        # todo 为方便调试暂时屏蔽登录逻辑，调试完成后需要修改
        # username = input('请输入用户名：')
        # password = input('请输入密码：')
        # return username, password
        return 'name', 'pass'

    def decodeinfo(self, s: str):
        return Coder.getBattleClass(s)

    def load_tankais(self):
        # ./tank目录专用于存放坦克AI程序，从该目录导入坦克AI程序
        p = Path('./tank')
        # 仅筛选出.py文件
        pyname = list(p.glob('*.py'))

        modules = []
        for fullname in pyname:
            name = Path(fullname).stem
            m = import_module(f'tank.{name}')
            # 排除其他非坦克AI的.py文件
            if 'AI' in dir(m):
                modules.append(m)
        return len(modules), modules


if __name__ == "__main__":
    Client()
