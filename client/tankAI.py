# coding:utf8
'''
author : Guoxi
email  : splinzer@gmail.com
time   : 2018 下午3:37
'''


# from multiprocessing import Connection
from time import sleep

class TankAI():
    """
    该类将tankAI中的战斗动作编码位如下字符串：
    name:t1|width:20|height:20|x:65|y:50|direction:4|velocity:5|type:tank|life:100|oil:100|weapon1:500|weapon2:500|status:4;
    name:t2|width:20|height:20|x:285|y:50|direction:3|velocity:5|type:tank|life:100|oil:100|weapon1:500|weapon2:500|status:4;
    name:t1_1|width:4|height:4|x:90|y:60|direction:4|velocity:10|type:bullet|weapon_type:500|status:4;
    name:t2_2|width:4|height:4|x:280|y:60|direction:3|velocity:10|type:bullet|weapon_type:500|status:4

    """
    WEAPON_1 = 1
    WEAPON_2 = 2

    # STATUS_READY 就绪状态
    # STATUS_DEAD 死亡状态，该状态的物体无法移动，且状态不再发生变化
    # STATUS_STOP 停止状态，除非状态被重置其他状态，否则物体会一直保持静止不动
    # STATUS_MOVING 移动中状态，除非碰撞到物体或边界，该状态的物体会一直按照其方向移动
    STATUS_READY = 1
    STATUS_DEAD = 2
    STATUS_STOP = 3
    STATUS_MOVING = 4

    MAX_VELOCITY = 5

    DIRECTION_UP = 1
    DIRECTION_DOWN = 2
    DIRECTION_LEFT = 3
    DIRECTION_RIGHT = 4

    def __init__(self, pipe, id):
        self.id = id
        self.pipe = pipe
        self.start()
        self.action = {}

        while True:
            print('阻塞')
            battleinfo = self.pipe.recv()
            print('tankAI收到',battleinfo)
            # 找到哪个坦克是自己的坦克
            self.find_myself(battleinfo)
            self.on_update(battleinfo)

            sleep(0.1)
            print('tank AI action', self.action)

    def find_myself(self, battleinfo):
        tanks = battleinfo.tanks
        for tank in tanks:
            if self.id == tank.name:
                self.mytank = tank
                break

    def start(self):
        pass

    def on_update(self, battle):
        pass

    def move(self, direction: int, velocity: int = 5):
        """
        按照指定方向和速度移动（会一直移动直到调用stop方法，或者发生碰撞）
        :param direction:移动方向
        :param velocity:移动速度
        """
        self.add_action('status', self.STATUS_MOVING)
        self.add_action('direction', direction)

    def fire(self, direction, weapon):
        self.add_action('fire', 'on')
        self.add_action('weapon', weapon)
        self.add_action('status', direction)

    def add_action(self, type, value):
        self.action.update({type: value})
