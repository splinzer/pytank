# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 下午6:30
from server.tank.tank import *
from server.tank.battlefield import *
from server.tank.point import Point
from server.tank.barrier import Barrier
from multiprocessing import Queue, Process
from server.websocket_server import SimpleBroadServer, SimpleWebSocketServer


def updateTanks(bt: Battlefield, queue: Queue):
    n = 400
    while n:
        bt.update()
        # n -= 1
        sleep(0.5)


def broadCast():
    server = SimpleWebSocketServer('', 8000, SimpleBroadServer)

    server.serveforever()


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

    q = Queue()
    update_p = Process(target=updateTanks, name='updateprocess', args=(bt, q))
    websocket_p = Process(target=None, name='websocket')

    update_p.start()
    websocket_p.start()

    update_p.join()
    websocket_p.join()


if __name__ == '__main__':
    main()
