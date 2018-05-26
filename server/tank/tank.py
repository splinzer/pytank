from server.tank.rectobject import *


class Tank(RectObject):
    """
    坦克类
    """
    WEAPON_HEAVY = 0
    WEAPON_LIGHT = 1
    WEAPON_HEAVY_ATTAK = 10
    WEAPON_LIGHT_ATTAK = 5

    def __init__(self, name: str, socket_addr: tuple = None):
        super().__init__(name=name, width=20, height=20, x=0, y=0)
        self.life = 100
        self.oil = 100
        self.weapon = Tank.WEAPON_HEAVY
        self.status = Tank.STATUS_READY
        self.socket_addr = socket_addr

    def get_life(self):
        return self.life

    def get_oil(self):
        return self.oil

    def get_weapon(self):
        return self.weapon

    def set_weapon(self, weapon_type: int = WEAPON_HEAVY):
        self.weapon = weapon_type


def main():
    t1 = Tank('t1')
    t1.set_position(50, 50)
    t1.set_status(Tank.STATUS_MOVING)
    t1.set_direction(Tank.DIRECTION_LEFT)
    for i in range(20):
        t1.update()


if __name__ == '__main__':
    main()
