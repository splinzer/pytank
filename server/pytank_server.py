# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 下午6:30
from server.tank.tank import *
from server.tank.battlefield import *
from server.tank.barrier import Barrier
from server.websocket_server import SimpleBroadServer, SimpleWebSocketServer
from multiprocessing import Queue, Process, Manager
from time import sleep, time
import os
import subprocess
from select import *
from socket import *
from random import randint
from server.tank.infocoder import InfoCoder

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


def start_websocket_server(queue: Queue):
    SimpleBroadServer.queue = queue
    SimpleBroadServer.framerate = FRAMERATE
    server = SimpleWebSocketServer(HOST, WEBSOCKET_PORT, SimpleBroadServer)
    open_websocket_client(WEBSOCKET_CLIENT_URL)
    server.serveforever()


def open_websocket_client(url):
    path = os.getcwd() + url
    subprocess.Popen(['chromium-browser', path])
    print('[server]打开<本地浏览器>')
    # os.system('chromium-browser ' + os.getcwd() + url + ' 2>/dev/null&')


class BattleManager:
    def __init__(self):
        self.battlefields = []

    def add_battlefield(self, bt: Battlefield):
        self.battlefields.append(bt)

    def remove_battlefield(self, bt: Battlefield):
        if len(self.battlefields):
            self.battlefields.remove(bt)


def main():
    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    # 启动websocket伺服进程
    websk_queue = Queue()
    websk_p = Process(target=start_websocket_server, args=(websk_queue,))
    websk_p.start()

    # 客户端地址和坦克名对应关系列表
    shared_memory = Manager()
    client_addrs_list = shared_memory.dict()
    # 战场情报输出队列
    out_queue = Queue()
    # 客户端指令输入队列
    in_queue = Queue()
    # 启动战场情报下发伺服进程
    send_p = Process(target=sendinfo_to_client, args=(s, out_queue, client_addrs_list))
    send_p.start()
    # todo 实现多个战斗同时进行
    while True:
        # 验证用户密码密码
        data, addr = s.recvfrom(1024)
        data = data.decode()

        if data == '':
            continue
        elif data[0:5] == 'LOGIN':
            username, password, count = data[5:].split('|')
            # 客户端身份验证（无数据或客户端用户名密码验证失败）
            if verify_user(username, password):
                # 按照客户端需要创建拥有指定坦克数量的战斗
                bt, tank_id_list = createBattle(int(count))
                # 客户端地址和坦克名对应关系列表，数据如下样例：
                # [('127.0.0.1',4957):['tank1','tank2'],
                #  ('127.0.0.1',4958):['tank1','tank2','tank2'],
                #  ('127.0.0.1',4959):['tank1','tank2','tank2']]
                client_addrs_list.update({addr: tank_id_list})
                # 告知客户端战斗已经成功创建（返回该战斗中包含的坦克的name列表）
                msg = 'ok|' + bt.id + '|' + '|'.join(tank_id_list)
                s.sendto(msg.encode(), addr)

                # 开启服务主循环
                main_p = Process(target=mainloop, args=(bt, [in_queue], [websk_queue, out_queue]))
                main_p.start()
        else:
            # 指令示例：{'weapon':2,'direction':2,'fire':'on','status':3}
            print('[server]收到<客户端指令>来自<{}>:{}'.format(addr, data))
            in_queue.put(data)
            sleep(FRAMERATE)

    os.wait()


def mainloop(bt: Battlefield, in_queues_list, out_queues_list):
    print('[server]启动<主进程循环>')
    while True:

        # 更新战场信息
        for q in in_queues_list:
            if not q.empty():
                bt.update(q.get())

        # 将战场信息放入消息队列
        for q in out_queues_list:
            q.put(bt)
        # 信息下发频率控制
        sleep(FRAMERATE)


def sendinfo_to_client(s: socket, queue: Queue, shared_memory):
    print('[server]启动<战场数据伺服进程>')
    while True:
        if not queue.empty():
            data = queue.get()
            coder = InfoCoder()
            data = coder.encoder(data)
            for addr in shared_memory.keys():
                s.sendto(data.encode(), addr)
                print('[server]下发<战场数据>给<{}>:{}'.format(addr, data))
        sleep(FRAMERATE)


def get_random_position(size: tuple):
    width = size[0]
    height = size[1]
    tank_width = 20
    tank_height = 20
    x = randint(tank_width, width - tank_width)
    y = randint(tank_height, height - tank_height)
    return x, y


def createBattle(tank_count: int):
    """
    创建拥有指定数量坦克的战场
    :param tank_count: 坦克数量
    :return: 元组，(战场对象，坦克name列表)
    """
    size = (600, 400)
    # 生成随机种子
    seed = '{}'.format(round(time()))

    bt = Battlefield(*size)
    # 生成战场唯一标识
    bt.id = 'b' + seed
    # todo 实现随机生成障碍物
    # bt.add_barrier(Barrier(20, 10, 100, 100))
    # bt.add_barrier(Barrier(10, 15, 300, 500))
    tank_id_list = []

    for i in range(1, tank_count + 1):
        tank_id = 't' + seed + str(i)
        tank_id_list.append(tank_id)
        tank = Tank(tank_id)
        # 设置坦克所属战场
        tank.battlefield_id = bt.id
        tank.set_position(*get_random_position(size))
        tank.set_status(Tank.STATUS_STOP)
        tank.set_direction(Tank.DIRECTION_RIGHT)
        bt.add_tank(tank)
    return bt, tank_id_list


def verify_user(username, password):
    # 验证用户名密码
    return True


if __name__ == '__main__':
    main()
