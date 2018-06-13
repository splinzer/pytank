from server.tank.battleobject import *
from server.tank.bullet import Bullet


class Tank(BattleObject):
    """
    坦克类
    """

    # todo bug：坦克相撞后仍能够继续移动的问题
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.type = 'tank'
        self.life = 100
        self.oil = 100
        self.ammo = 500
        self.status = self.STATUS_MOVING

        self.socket_addr = None

    def is_bullet_empty(self):
        """
        检查是否没子弹了
        :return:
        """
        if self.ammo == 0:
            return True
        else:
            return False

    def loss_life(self, n):
        """
        减去n点血，坦克被击中时使用该方法减血
        :param n: 要减去的点数
        :return:
        """
        self.life -= n
        # 当生命为0，坦克over
        if self.life <= 0:
            self.suicide()

    def use_one_bullet(self):
        if self.ammo != 0:
            self.ammo -= 1

    def set_socket_addr(self, socket_addr: tuple):
        self.socket_addr = socket_addr

    def get_socket_addr(self):
        return self.socket_addr

    def get_battlefield(self):
        return self.battlefield

    def set_battlefield(self, bt):
        self.battlefield = bt

    def get_life(self):
        return self.life

    def get_oil(self):
        return self.oil

    def fire(self):
        # 有弹药且坦克生存时才能射击
        if not self.is_bullet_empty() and not self.dead:

            bullet = Bullet(owner_id=self.id, battlefield=self.battlefield, owner=self)
            # bullet.set_position(*self.get_center())
            #
            # bullet.set_direction(self.direction)
            bullet.set_status(self.STATUS_MOVING)
            self.battlefield.add_bullet(bullet)
            self.use_one_bullet()

    def limit_bound(self, delta=7) -> bool:
        """
        检测对象是否到达战场边沿，是的话将对象的阻塞状态设置为True
        :param delta:定义偏移量，如果对象碰到边界，则按照该偏移量反弹，目的是避免物体被困住。
        :return:布尔值，在战场边沿为True
        """
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
            self.set_position(n_x, n_y)
            self.set_status(self.STATUS_STOP)

            self.block = True
            return True

        self.block = False
        return False
