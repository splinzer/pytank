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

# 观战网页文件的本地地址
WEBSOCKET_CLIENT_URL = '/client/websocket.html'
# 战场更新频率
FRAMERATE = 0.1


def updateTanks(bt: Battlefield):
    q = Queue()
    websocket_p = Process(target=start_websocket_server, name='websocket', args=(q,))
    websocket_p.start()

    n = 400
    while n:
        bt.update()
        q.put(bt)
        # n -= 1
        sleep(FRAMERATE)


def start_websocket_server(queue: Queue):
    SimpleBroadServer.queue = queue
    SimpleBroadServer.framerate = FRAMERATE
    server = SimpleWebSocketServer('', 8000, SimpleBroadServer)
    open_websocket_client(WEBSOCKET_CLIENT_URL)
    server.serveforever()


def open_websocket_client(url):
    print('打开本地浏览器')
    os.system('chromium-browser ' + os.getcwd() + url + '&')


def main():
    bt = Battlefield(600, 400)
    # bt.add_barrier(Barrier(20, 10, 100, 100))
    # bt.add_barrier(Barrier(10, 15, 300, 500))
    t1 = Tank('t1', ('127.0.0.1', 7777))
    t1.set_position(50, 50)
    t1.set_status(Tank.STATUS_MOVING)
    t1.set_direction(Tank.DIRECTION_RIGHT)

    t2 = Tank('t2', ('127.0.0.1', 7778))
    t2.set_position(300, 50)
    t2.set_status(Tank.STATUS_MOVING)
    t2.set_direction(Tank.DIRECTION_LEFT)

    bt.add_tank(t1)
    bt.add_tank(t2)

    update_p = Process(target=updateTanks, name='updateprocess', args=(bt,))
    update_p.start()
    update_p.join()


if __name__ == '__main__':
    main()
