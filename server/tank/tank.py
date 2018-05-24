from server.tank.rectobject import RectObject
from server.tank.point import Point

WEAPON_HEAVY = 0
WEAPON_LIGHT = 1
WEAPON_HEAVY_ATTAK = 10
WEAPON_LIGHT_ATTAK = 5

STATUS_READY = 0
STATUS_DEAD = 1
STATUS_STOP = 2
STATUS_MOVING = 3

MAX_VELOCITY = 5

DIRECTION_UP = 0
DIRECTION_DOWN = 1
DIRECTION_LEFT = 2
DIRECTION_RIGHT = 3


class Tank(RectObject):
    """
    坦克类
    """

    def __init__(self, name: str, socket_addr: tuple = None):
        super().__init__(width=20, height=20, position=Point(0, 0))
        self.name = name
        self.life = 100
        self.oil = 100
        self.weapon = WEAPON_HEAVY
        self.status = STATUS_READY
        self.socket_addr = socket_addr
        self.direction = DIRECTION_UP
        self.velocity = MAX_VELOCITY

    def get_velocity(self):
        return self.velocity

    def set_velocity(self, velocity: int):
        self.velocity = velocity

    def get_direction(self):
        return self.direction

    def set_direction(self, direction: int):
        self.direction = direction

    def get_name(self):
        return self.name

    def get_life(self):
        return self.life

    def get_oil(self):
        return self.oil

    def get_weapon(self):
        return self.weapon

    def set_weapon(self, weapon_type: int = WEAPON_HEAVY):
        self.weapon = weapon_type

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def stop(self):
        self.set_status(STATUS_STOP)

    def ready(self):
        self.set_status(STATUS_READY)

    def move_step(self, direction: int, velocity: int = 5):
        """
        坦克按照指定方向和速度移动一次
        :param direction:移动方向
        :param velocity:移动速度
        :return:新坐标（Point类型）
        """
        x = self.position.x
        y = self.position.y
        if velocity > MAX_VELOCITY:
            velocity = MAX_VELOCITY
        if direction == DIRECTION_UP:
            y -= velocity
        elif direction == DIRECTION_DOWN:
            y += velocity
        elif direction == DIRECTION_LEFT:
            x -= velocity
        elif direction == DIRECTION_RIGHT:
            x += velocity

        self.set_position(x, y)

    def move(self, direction: int, velocity: int = 5):
        pass

    def update(self):
        if self.status == STATUS_MOVING:
            self.move_step(self.direction, self.velocity)
        print(self.name, self.position.x, self.position.y)


def main():
    t1 = Tank('t1')
    t1.set_position(50, 50)
    t1.set_status(STATUS_MOVING)
    t1.set_direction(DIRECTION_LEFT)
    for i in range(20):
        t1.update()


if __name__ == '__main__':
    main()
