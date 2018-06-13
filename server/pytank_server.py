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
import json
import zlib

# 战场更新频率
FRAMERATE = 0.1
# webscoket服务器host
HOST = ''
# socket服务端口
PORT = 9000
# webscoket服务器端口
WEBSOCKET_PORT = 8000
# 观战网页文件的本地地址
# WEBSOCKET_CLIENT_URL = '/client/websocket.html'
WEBSOCKET_CLIENT_URL = '/client/webworker.html'
# 缓冲区大小
BUFFER_SIZE = 2096


# todo bug:战斗接收后服务端仍在给客户端发消息

class GameServer:

    def __init__(self):
        s = socket(AF_INET, SOCK_DGRAM)
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        # 启动websocket伺服进程
        websk_queue = Queue()
        websk_p = Process(target=self.start_websocket_server, args=(websk_queue,))
        websk_p.daemon = True
        websk_p.start()

        # 创建进程内存共享对象
        shared_memory = Manager()

        # 客户端地址和坦克名对应关系列表
        client_list_shared = shared_memory.dict()

        # 战场对象列表
        battle_list_shared = shared_memory.dict()

        # 战场情报输出队列
        out_queue = Queue()
        # 客户端指令输入队列
        in_queue = Queue()

        # 开启服务主循环
        # websk_queue,out_queue接收相同的战场数据
        main_p = Process(target=self.mainloop, args=(battle_list_shared, [in_queue], [websk_queue, out_queue]))
        main_p.daemon = True
        main_p.start()

        # 启动战场情报下发伺服进程：将战场数据发给客户端
        send_p = Process(target=self.sendinfo_to_client, args=(s, out_queue, client_list_shared))
        send_p.daemon = True
        send_p.start()

        # todo 实现多个战斗同时进行
        while True:
            print(battle_list_shared)

            # 验证用户密码
            data, addr = s.recvfrom(BUFFER_SIZE)
            data = data.decode()

            if data == '':
                continue
            elif data[0:5] == 'LOGIN':
                username, password, count = data[5:].split('|')
                # 客户端身份验证（无数据或客户端用户名密码验证失败）
                if self.verify_user(username, password):
                    print(f'[server]登录成功<客户端>来自<{addr}>:{data}')
                    # 按照客户端需要创建拥有指定坦克数量的战斗
                    bt, tank_id_list = self.createBattle(int(count))
                    # 战场对象存入共享对象
                    battle_list_shared.update({bt.id: bt})
                    print(f'[server]共享对象值：{battle_list_shared}')
                    # 客户端地址和坦克名对应关系列表，数据如下样例：
                    # [('127.0.0.1',4957):['tank1','tank2'],
                    #  ('127.0.0.1',4958):['tank1','tank2','tank2'],
                    #  ('127.0.0.1',4959):['tank1','tank2','tank2']]
                    client_list_shared.update({addr: tank_id_list})
                    # 告知客户端战斗已经成功创建（返回该战斗中包含的坦克的name列表）
                    msg = 'ok|' + bt.id + '|' + '|'.join(tank_id_list)
                    s.sendto(msg.encode(), addr)


            else:
                # 指令示例：{'weapon':2,'direction':2,'fire':'on','status':3}
                # print(f'[server]收到<客户端指令>来自<{addr}>:{data}')
                # 把客户端指令存入消息队列，有mainloop进程进行处理
                in_queue.put(data)
                sleep(FRAMERATE)

    def mainloop(self, battle_list_shared, in_queues_list, out_queues_list):
        """
        根据客户端传回的指令更新战场信息
        :param battle_list_shared:所有战场共享内存对象
        :param in_queues_list:输入指令队列列表
        :param out_queues_list:输出指令队列列表
        :return:
        """
        print('[server]启动<mainloop进程>')

        while True:

            # 需要首先将战场信息发到客户端（避免服务端和客户端都会等待阻塞）
            for out_q in out_queues_list:
                for bt in battle_list_shared.values():
                    # 将战场信息放入消息队列
                    out_q.put(bt)

            # 根据客户端传回来的指令对各战场进行运算，将计算结果放入out_queue队列，由sendinfo_to_client负责发送
            # todo 客户端无指令的情况下，战场应该也能够运算并下发数据
            for in_q in in_queues_list:

                if not in_q.empty():
                    # 取出指令，示例格式："{'battle_id':'b20340','id':'t20394','weapon':2,'direction':2,'fire':'on','status':3}"
                    battleinfo = in_q.get()
                    # print(f'[server]指令:{battleinfo}')
                    # 将序列化的指令恢复成tank对象
                    tankinfo = json.loads(battleinfo)
                    # 在客户端启动之初，会因收到不完整的指令导致错误，这里使用需要异常处理

                    # 更新对应战场的数据
                    if tankinfo['battle_id'] in battle_list_shared.keys():
                        # print(f'[server]战场数据更新<{tankinfo}>')
                        bt = battle_list_shared[tankinfo['battle_id']]
                        # 根据客户端传来的指令更新对应战场
                        bt.update_before_send(tankinfo)

                        # 注意，这行代码看似多余，其实是为了避免一个Manager的bug
                        # 这个bug是说Manager对象无法监测到它引用的可变对象值的修改，需要通过调用__setitem__方法来让它获得通知
                        # 详情参考python官方文档中关于包含像list dict等可变对象时的特殊处理
                        # https://docs.python.org/3.6/library/multiprocessing.html?highlight=multiprocess#proxy-objects
                        battle_list_shared[tankinfo['battle_id']] = bt

                        # 如果战斗已经结束且已通知客户端，则从战斗列表中删除该战斗对象
                        if bt.gameover and bt.gameover_sended:
                            del battle_list_shared[tankinfo['battle_id']]

                else:
                    # 客户端无指令的情况
                    # 更新对应战场的数据
                    for id in battle_list_shared.keys():
                        bt = battle_list_shared[id]
                        # 更新战场
                        bt.update_before_send()
                        battle_list_shared[id] = bt
                        # 如果战斗已经结束且已通知客户端，则从战斗列表中删除该战斗对象
                        if bt.gameover and bt.gameover_sended:
                            del battle_list_shared[id]
            # 信息下发频率控制
            sleep(FRAMERATE)


    def sendinfo_to_client(self, s: socket, out_queue: Queue, client_list_shared):
        """
        从输出消息队列中读取消息并发给各个客户端
        :param s: 主服务socket
        :param out_queue: 输出消息队列
        :param client_list_shared: 客户端列表共享对象
        :return:
        """
        print('[server]启动<战场数据伺服进程>')
        while True:
            if not out_queue.empty():
                data = out_queue.get()
                coder = InfoCoder()
                data = coder.encoder(data)
                for addr in client_list_shared.keys():
                    # print('[server]下发<战场数据>给<{}>:{}'.format(addr, data))
                    # 传之前先对数据进行压缩
                    data = zlib.compress(data.encode())
                    # 将数据发送给客户端
                    s.sendto(data, addr)

            sleep(FRAMERATE)

    def start_websocket_server(self, queue: Queue):
        SimpleBroadServer.queue = queue
        SimpleBroadServer.framerate = FRAMERATE
        server = SimpleWebSocketServer(HOST, WEBSOCKET_PORT, SimpleBroadServer)
        self.open_websocket_client(WEBSOCKET_CLIENT_URL)
        server.serveforever()

    def open_websocket_client(self, url):
        path = os.getcwd() + url
        subprocess.Popen(['chromium-browser', path])
        print('[server]打开<本地浏览器>')
        # os.system('chromium-browser ' + os.getcwd() + url + ' 2>/dev/null&')

    def get_random_position(self, battle_size: tuple, tank_size: tuple):
        width = battle_size[0]
        height = battle_size[1]
        tank_width = tank_size[0]
        tank_height = tank_size[1]
        x = randint(tank_width, width - tank_width)
        y = randint(tank_height, height - tank_height)
        return x, y

    def createBattle(self, tank_count: int):
        """
        创建拥有指定数量坦克的战场
        :param tank_count: 坦克数量
        :return: 元组，(战场对象，坦克name列表)
        """
        battle_size = (800, 600)
        # 生成随机种子
        seed = '{}'.format(round(time()))

        bt = Battlefield(*battle_size)
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
            tank.battlefield = bt

            tank.set_position(*self.get_random_position(battle_size, (tank.width, tank.height)))
            tank.set_status(Tank.STATUS_MOVING)
            tank.set_direction(Tank.DIRECTION_RIGHT)
            bt.add_tank(tank)
        return bt, tank_id_list

    def verify_user(self, username, password):
        # 验证用户名密码
        return True


if __name__ == '__main__':
    GameServer()
