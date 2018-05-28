# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 下午6:30
from server.tank.tank import *
from server.tank.battlefield import *
from server.tank.barrier import Barrier
from server.websocket_server import SimpleBroadServer, SimpleWebSocketServer
from multiprocessing import Queue, Process
from time import sleep
import os

# 战场更新频率
FRAMERATE = 0.1
# webscoket服务器host
WEBSOCKET_HOST = ''
# webscoket服务器端口
WEBSOCKET_PORT = 8000
# 观战网页文件的本地地址
WEBSOCKET_CLIENT_URL = '/client/websocket.html'


def mainloop(bt: Battlefield):
    q = Queue()
    # 通过websocket server对外提供战场信息更新
    websocket_p = Process(target=start_websocket_server, name='websocket', args=(q,))
    websocket_p.start()

    while True:
        # 更新战场信息
        bt.update()
        # 存入要广播出去的战场信息
        q.put(bt)

        sleep(FRAMERATE)


def start_websocket_server(queue: Queue):
    SimpleBroadServer.queue = queue
    SimpleBroadServer.framerate = FRAMERATE
    server = SimpleWebSocketServer(WEBSOCKET_HOST, WEBSOCKET_PORT, SimpleBroadServer)
    open_websocket_client(WEBSOCKET_CLIENT_URL)
    server.serveforever()


def open_websocket_client(url):
    print('打开本地浏览器')
    os.system('chromium-browser ' + os.getcwd() + url + ' 2>/dev/null&')


def main():
    bt = Battlefield(600, 400)
    # bt.add_barrier(Barrier(20, 10, 100, 100))
    # bt.add_barrier(Barrier(10, 15, 300, 500))
    t1 = Tank('t1')
    t1.set_position(50, 50)
    t1.set_status(Tank.STATUS_MOVING)
    t1.set_direction(Tank.DIRECTION_RIGHT)

    t2 = Tank('t2')
    t2.set_position(300, 50)
    t2.set_status(Tank.STATUS_MOVING)
    t2.set_direction(Tank.DIRECTION_LEFT)

    bt.add_tank(t1)
    bt.add_tank(t2)

    t1.fire(t1.weapon1)
    t2.fire(t2.weapon2)

    main_p = Process(target=mainloop, args=(bt,))
    main_p.start()
    main_p.join()


if __name__ == '__main__':
    main()
