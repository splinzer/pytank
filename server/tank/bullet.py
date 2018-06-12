# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 上午8:56
from server.tank.battleobject import *


class Bullet(BattleObject):
    """
    子弹类
    """
    __no__ = 1

    def __init__(self, owner_id, battlefield, owner: BattleObject):
        super().__init__(width=4, height=4, x=0, y=0)
        self.id = '{}_{}'.format(owner_id, Bullet.__no__)
        Bullet.__no__ += 1
        self.type = 'bullet'
        self.owner = owner
        self.set_position(*self.get_fire_position())
        self.set_direction(owner.get_direction())
        self.battlefield = battlefield
        self.battlefield_id = battlefield.id
        self.velocity = 12

    def get_fire_position(self):
        """
        根据坦克的位置和方向计算子弹的发射位置
        """
        x = self.owner.x
        y = self.owner.y
        w = self.owner.width / 2
        h = self.owner.height / 2
        if self.owner.direction == self.DIRECTION_UP:
            y -= h
        elif self.owner.direction == self.DIRECTION_DOWN:
            y += h
        elif self.owner.direction == self.DIRECTION_RIGHT:
            x += w
        elif self.owner.direction == self.DIRECTION_LEFT:
            x -= w
        return x, y


def main():
    pass


if __name__ == '__main__':
    main()
