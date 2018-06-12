from server.tank.battleobject import *
from server.tank.bullet import Bullet


class Tank(BattleObject):
    """
    坦克类
    """

    def __init__(self, id):
        super().__init__()
        self.id = id
        self.type = 'tank'
        self.life = 100
        self.oil = 100
        self.ammo = 500
        self.status = self.STATUS_READY

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
        if not self.is_bullet_empty():
            # todo 实现发射
            print('###############射击')
            bullet = Bullet(owner_id=self.id, battlefield=self.battlefield, owner = self)
            # bullet.set_position(*self.get_center())
            #
            # bullet.set_direction(self.direction)
            bullet.set_status(self.STATUS_MOVING)
            self.battlefield.add_bullet(bullet)
            self.use_one_bullet()


def main():
    t1 = Tank('t1')
    t1.set_position(50, 50)
    t1.set_status(Tank.STATUS_MOVING)
    t1.set_direction(Tank.DIRECTION_LEFT)
    for i in range(20):
        t1.update()


if __name__ == '__main__':
    main()
