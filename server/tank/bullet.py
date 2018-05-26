# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 上午8:56
from server.tank.rectobject import *


class Bullet(RectObject):
    """
    子弹类
    """

    def __init__(self, name: str, owner: str, socket_addr: tuple = None):
        super().__init__(name=name, width=20, height=20, x=0, y=0)


def main():
    t1 = Bullet('t1')
    t1.set_position(50, 50)
    t1.set_status(STATUS_MOVING)
    t1.set_direction(DIRECTION_LEFT)
    for i in range(20):
        t1.update()


if __name__ == '__main__':
    main()
