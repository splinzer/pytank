from server.tank.rectobject import *
from server.tank.bullet import Bullet


class Tank(RectObject):
    """
    坦克类
    """
    WEAPON_1 = 1
    WEAPON_2 = 2

    def __init__(self, name: str):
        super().__init__(width=20, height=20, x=0, y=0)
        self.name = name
        self.type = 'tank'
        self.life = 100
        self.oil = 100
        self.weapon1 = 500
        self.weapon2 = 500
        self.status = self.STATUS_READY
        self.socket_addr = None
        # 坦克所在战场
        self.battlefield = None

    def is_bullet_empty(self, weapon: 'weapon type'):
        """
        检查是否没子弹了
        :param weapon:
        :return:
        """
        if weapon == self.WEAPON_1 and self.weapon1 == 0:
            return True
        elif weapon == self.WEAPON_2 and self.weapon2 == 0:
            return True
        else:
            return False

    def use_one_bullet(self, weapon):
        if weapon == self.WEAPON_1 and self.weapon1 == 0:
            self.weapon1 -= 1
        elif weapon == self.WEAPON_2 and self.weapon2 == 0:
            self.weapon2 -= 1

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

    def fire(self, weapon: 'weapon type'):
        if not self.is_bullet_empty(weapon):
            bullet = Bullet(owner=self.name)
            bullet.set_position(*self.get_center())
            bullet.set_type(weapon)
            bullet.set_direction(self.direction)
            bullet.set_status(self.STATUS_MOVING)
            self.battlefield.add_bullet(bullet)
            self.use_one_bullet(weapon)


def main():
    t1 = Tank('t1')
    t1.set_position(50, 50)
    t1.set_status(Tank.STATUS_MOVING)
    t1.set_direction(Tank.DIRECTION_LEFT)
    for i in range(20):
        t1.update()


if __name__ == '__main__':
    main()
