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


# 战场更新频率
FRAMERATE = 0.1
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


class Client:
    def __init__(self):
        # self.pipes = []
        self.in_queues = []
        self.out_queues = []
        self.s = None
        self.connect()

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
            # 服务器响应 ok|tank1|tank2|tank3|...
            response = self.s.recv(1024).decode()
            response = response.split('|')
            if response[0] == 'ok':
                self.init_tanks(response[1:])
                break
            else:
                continue
        # 主循环

        while True:
            # 接收服务端战场信息
            data = self.s.recv(1024)
            print('来自服务器的战场数据>>', data)
            # 判断游戏结束
            if data == 'over':
                # todo 显示游戏结果
                pass

            data = data.decode()
            # 将信息转发给各坦克
            for in_queue in self.in_queues:
                # 反序列化info
                in_queue.put(self.decodeinfo(data))
            # 获取各坦克的指令发给服务器
            for out_queue in self.out_queues:
                if not out_queue.empty():
                    bt = out_queue.get()
                    # todo 发送前需添加tank和战场签名
                    self.send_to_server(bt)
                else:
                    print('客户端无指令发出')
        os.wait()

    def send_to_server(self, bt):
        info = json.dumps(bt)
        print('客户端指令>>', info)
        self.s.send(info.encode())

    def check_tankAIs(self, tank_count):
        if ALLOW_COUNT[0] > tank_count > ALLOW_COUNT[1]:
            sys.exit(f'坦克AI数量必须在{ALLOW_COUNT}个内')

    def init_tanks(self, name_list: list):
        n = 0
        for m in self.tankAIs:

            in_queue = Queue()
            self.in_queues.append(in_queue)
            out_queue = Queue()
            self.out_queues.append(out_queue)

            p = Process(target=m.AI, args=(in_queue, out_queue, name_list[n]))
            p.start()
            n += 1

    def getverifyinfo(self):
        # todo 调试完成后需要修改登录逻辑
        # username = input('请输入用户名：')
        # password = input('请输入密码：')
        # return username, password
        return 'name','pass'

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
