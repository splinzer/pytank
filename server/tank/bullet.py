# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 上午8:56
from server.tank.rectobject import *


class Bullet(RectObject):
    """
    子弹类
    """
    WEAPON_1 = 0
    WEAPON_2 = 1
    MAX_VELOCITY = 10
    __no__ = 1

    def __init__(self, owner: str):
        super().__init__(width=4, height=4, x=0, y=0)
        self.name = '{}_{}'.format(owner, Bullet.__no__)
        Bullet.__no__ += 1
        self.type = 'Bullet'
        self.weapon_type = Bullet.WEAPON_1

    def set_type(self, weapon: 'weapon type'):
        self.weapon_type = weapon


def main():
    pass


if __name__ == '__main__':
    main()
