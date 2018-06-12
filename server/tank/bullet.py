# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 上午8:56
from server.tank.battleobject import *


class Bullet(BattleObject):
    """
    子弹类
    """
    MAX_VELOCITY = 10
    __no__ = 1

    def __init__(self, owner: str):
        super().__init__(width=4, height=4, x=0, y=0)
        self.name = '{}_{}'.format(owner, Bullet.__no__)
        Bullet.__no__ += 1
        self.type = 'bullet'


def main():
    pass


if __name__ == '__main__':
    main()
