# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 下午6:30
from server.tank.tank import *
from server.tank.battlefield import *
from server.tank.point import Point
from server.tank.barrier import Barrier
from server.websocket_server import SimpleBroadServer, SimpleWebSocketServer
from multiprocessing import Queue, Process
import os

WEBSOCKET_CLIENT_URL = '../client/websocket.html'

def updateTanks(bt: Battlefield):
    q = Queue()
    websocket_p = Process(target=start_websocket_server, name='websocket', args=(q,))
    websocket_p.start()

    n = 400
    while n:
        bt.update()
        q.put(bt)
        # n -= 1
        sleep(0.5)


def start_websocket_server(queue: Queue):
    SimpleBroadServer.queue = queue
    server = SimpleWebSocketServer('', 8000, SimpleBroadServer)
    open_websocket_client(WEBSOCKET_CLIENT_URL)
    server.serveforever()

def open_websocket_client(url):
    os.popen('chromium-browser ' + url+'&')

def main():
    bt = Battlefield(600, 400)
    bt.add_barrier(Barrier(20, 10, Point(100, 100)))
    bt.add_barrier(Barrier(10, 15, Point(300, 500)))
    t1 = Tank('t1', ('127.0.0.1', 7777))
    t1.set_position(50, 50)
    t1.set_status(STATUS_MOVING)
    t1.set_direction(DIRECTION_LEFT)

    t2 = Tank('t2', ('127.0.0.1', 7778))
    t2.set_position(300, 50)
    t2.set_status(STATUS_MOVING)
    t2.set_direction(DIRECTION_RIGHT)

    bt.add_tank(t1)
    bt.add_tank(t2)

    update_p = Process(target=updateTanks, name='updateprocess', args=(bt,))
    update_p.start()
    update_p.join()



if __name__ == '__main__':
    main()
