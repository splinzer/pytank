# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 上午8:56
from server.tank.battleobject import *


class Bullet(BattleObject):
    """
    子弹类
    """
    # todo bug:子弹消失后仍然具有杀伤力，需要在子弹消失后清理掉
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
        self.velocity = 30

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

    def limit_bound(self, delta=7) -> bool:
        pos = self.get_position()
        x = pos[0]
        y = pos[1]
        width = self.width
        height = self.height
        # 定义偏移量，如果对象碰到边界，则按照该偏移量反弹，目的是避免物体被困住。
        delta = 7
        # n_x和n_y是发生碰到边界时反弹后物体的新坐标
        n_x = x
        n_y = y

        if x <= width / 2:
            n_x = x + delta

        if (x + width / 2) >= self.battlefield.width:
            n_x = x - delta

        if y <= height / 2:
            n_y = y + delta

        if (y + height / 2) >= self.battlefield.height:
            n_y = y - delta
        # 发生反弹位移，说明已经碰到了边界
        if (n_x, n_y) != (x, y):
            # 反弹
            self.set_status(self.STATUS_STOP)
            self.die()
            self.block = True
            return True

        self.block = False
        return False

