class Tank():
    WEAPON_HEAVY = 0
    WEAPON_LIGHT = 1
    WEAPON_HEAVY_ATTAK = 10
    WEAPON_LIGHT_ATTAK = 5
    STATUS_OK = 0
    STATUS_DEAD = 1
    STATUS_STOP = 2

    def __init__(self, name: str, socket_addr: tuple):
        self.width = 20
        self.height = 20
        self.name = name
        self.life = 100
        self.oil = 100
        self.position = (0, 0)
        self.weapon = self.WEAPON_HEAVY
        self.status = self.STATUS_OK
        self.socket_addr = socket_addr

    def get_name(self):
        return self.name

    def get_life(self):
        return self.life

    def get_oil(self):
        return self.oil

    def get_position(self):
        return self.position

    def set_position(self, x, y):
        self.position = (x, y)

    def get_weapon(self):
        return self.weapon

    def set_weapon(self, weapon_type: int = WEAPON_HEAVY):
        self.weapon = weapon_type

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def move_to(self, target: tuple, velocity: int = 5):
        pass
