# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 下午6:30
from server.tank.tank import *
from server.tank.battlefield import *
from server.tank.barrier import Barrier
from multiprocessing import Queue, Process, Manager
from time import sleep, time
import os
from select import *
from socket import *
from random import randint
from server.tank.infocoder import InfoCoder
import json
import zlib

# 战场更新频率
FRAMERATE = 0.1
# 服务ip
HOST = '176.234.96.91'
# 服务端口
PORT = 9000
# 缓冲区大小
BUFFER_SIZE = 2096


# todo bug:战斗接收后服务端仍在给客户端发消息

class GameServer:

    def __init__(self):
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind((HOST, PORT))

        # 创建进程内存共享对象
        shared_memory = Manager()

        # 进程共享对象：战场id和客户端地址对应关系字典
        # 形如：{'b1528977296': ('127.0.0.1', 44436)}
        self.bid_to_addr_shared = shared_memory.dict()

        # 进程共享对象：战场id和战场对象字典
        # 形如：{'b1528977296': <server.tank.battlefield.Battlefield object at 0x7f88fb1bbb70>}
        self.bid_to_battle_shared = shared_memory.dict()

        # 战场情报输出队列
        self.out_queue = Queue()
        # 客户端指令输入队列
        self.in_queue = Queue()

        # 该进程解析客户端传回的指令，并更新战场信息
        main_p = Process(target=self.mainloop)
        main_p.daemon = True
        main_p.start()

        # 该进程将战场数据发给客户端
        send_p = Process(target=self.sendinfo_to_client)
        send_p.daemon = True
        send_p.start()



        # todo 实现多个战斗同时进行
        # 服务端使用客户端的ip和端口号作为客户端唯一标识，每次客户端传给服务端的消息头部都加上该标识
        # 等待获取客户端登录请求，验证通过后，按照客户端要求创建战斗并给到客户端反馈
        '''
        客户端登录验证过程：
        1.客户端发出登录指令：LOGINusername|password|count
        2.服务端提取前5个字符，判断为LOGIN动作
        3.服务端验证username和password是否有效，无效重启验证过程，有效继续下一步
        4.服务端创建战斗，坦克数量使用count
        5.服务端存储战斗和客户端对应关系
        6.服务端反馈战斗创建成功消息给客户端：ok|b209203420|t234202|t230920|t224092
        
        '''
        while True:
            # print(f'[server]战场字典:{self.bid_to_battle_shared}')
            print(f'[server]客户端字典:{self.bid_to_addr_shared}')
            # 验证用户密码
            data, addr = self.sock.recvfrom(BUFFER_SIZE)
            # 以addr作为客户端唯一标识，形如：('127.0.0.1', 39194) ('127.0.0.1', 48078)
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

                    # 更新共享对象
                    self.bid_to_battle_shared.update({bt.id: bt})

                    self.bid_to_addr_shared.update({bt.id: addr})

                    # 告知客户端战斗已经成功创建（返回该战斗中包含的坦克的id列表）
                    msg = 'ok|' + bt.id + '|' + '|'.join(tank_id_list)

                    # 回执发送给客户端
                    self.sock.sendto(msg.encode(), addr)
                else:
                    continue

            elif data[0:8] == 'GAMEOVER':
                for _bid, _addr in self.bid_to_addr_shared.items():
                    if addr == addr:
                        self.close_battle(_bid)

            else:
                # 指令示例：{'weapon':2,'direction':2,'fire':'on','status':3}
                # print(f'[server]收到<客户端指令>来自<{addr}>:{data}')
                # 把客户端指令存入消息队列，由mainloop进程进行处理

                # 只接收已建立过连接的客户端数据
                if self.is_connected(addr):
                    self.in_queue.put(data)

                sleep(FRAMERATE)

    def is_connected(self, addr: tuple):
        """
        判断客户端是否已与服务器建立了连接
        :param addr:客户端ip和端口
        :return:
        """
        return addr in self.bid_to_addr_shared.values()
        pass

    def close_battle(self, battle_id):
        """
        当某个战斗结束时，做善后处理
        :return:
        """
        # 从共享对象中清除该战斗
        del self.bid_to_addr_shared[battle_id]
        del self.bid_to_battle_shared[battle_id]

    def verify_user(self, username, password):
        # 验证用户名密码
        # todo 用户登录验证
        return True

    def mainloop(self):
        """
        根据客户端传回的指令更新战场信息
        :return:
        """
        # todo 多战斗同时进行时的卡顿问题
        in_queues_list = [self.in_queue]
        out_queues_list = [self.out_queue]

        while True:

            # 需要首先将战场信息放入输出队列（避免服务端和客户端都会等待阻塞）

            for bt in self.bid_to_battle_shared.values():
                # 将战场信息放入消息队列
                self.out_queue.put(bt)

            # 根据客户端传回来的指令对各战场进行运算，由sendinfo_to_client负责从输出队列中提取战场信息并发送给客户端
            if not self.in_queue.empty():
                # 取出指令，示例格式："{'battle_id':'b20340','id':'t20394','weapon':2,'direction':2,'fire':'on','status':3}"
                battleinfo = self.in_queue.get()
                # 将序列化的指令恢复成tank对象
                tankinfo = json.loads(battleinfo)
                # 在客户端启动之初，会因收到不完整的指令导致错误，这里使用需要异常处理

                # 更新对应战场的数据
                if tankinfo['battle_id'] in self.bid_to_battle_shared.keys():
                    # print(f'[server]战场数据更新<{tankinfo}>')
                    bt = self.bid_to_battle_shared[tankinfo['battle_id']]
                    # 根据客户端传来的指令更新对应战场
                    bt.update_before_send(tankinfo)

                    # 注意，这行代码看似多余，其实是为了避免一个Manager的bug
                    # 这个bug是说Manager对象无法监测到它引用的可变对象值的修改，需要通过调用__setitem__方法来让它获得通知
                    # 详情参考python官方文档中关于包含像list dict等可变对象时的特殊处理
                    # https://docs.python.org/3.6/library/multiprocessing.html?highlight=multiprocess#proxy-objects
                    self.bid_to_battle_shared[tankinfo['battle_id']] = bt


            else:
                # 客户端无指令的情况
                # 更新对应战场的数据
                for id in self.bid_to_battle_shared.keys():
                    bt = self.bid_to_battle_shared[id]
                    # 更新战场
                    bt.update_before_send()
                    self.bid_to_battle_shared[id] = bt

            # 信息下发频率控制
            sleep(FRAMERATE)

    def sendinfo_to_client(self):
        """
        从输出消息队列中读取消息并发给各个客户端
        :return:
        """
        print('[server]启动<战场数据伺服进程>')
        while True:
            if not self.out_queue.empty():
                bt = self.out_queue.get()
                bid = bt.id
                if bid in self.bid_to_addr_shared:
                    coder = InfoCoder()
                    tank_info = coder.encoder(bt)
                    # 传之前先对数据进行压缩
                    tank_info = zlib.compress(tank_info.encode())
                    # 将数据发送给客户端
                    self.sock.sendto(tank_info, self.bid_to_addr_shared[bid])

                # for addr in self.bid_to_addr_shared.keys():
                #     # todo Bug：数据没有根据不同的战场分别发出，无法适应多战斗场景
                #     # print('[server]下发<战场数据>给<{}>:{}'.format(addr, data))
                #     # 传之前先对数据进行压缩
                #     tank_info = zlib.compress(tank_info.encode())
                #     # 将数据发送给客户端
                #     self.sock.sendto(tank_info, addr)

            sleep(FRAMERATE)

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


if __name__ == '__main__':
    GameServer()
