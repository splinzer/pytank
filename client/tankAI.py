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
    该类作为坦克控制类的超类，封装了一些底层方法，并提供了以下属性和方法便于编写控制逻辑

    以下battle对象用于获取战场信息：

        battle─┬───width（战场宽度）
               │
               ├───height（战场高度）
               │
               │ （坦克列表）
               ├───tanks─────┬───tank─┬───width
               │                      │
               │                      ├───height
               │                      ├───x
               │                      ├───y
               │                      ├───status
               │                      ├───life
               │                      ├───weapon
               │                      ├───oil
               │
               │
               ├───bullets──
               └───barriers───


    以下方法用于控制坦克进行战斗：

        TankAI.move          向指定方向持续移动（速度默认5）
        TankAI.stop_move     停止移动
        TankAI.fire          使用指定武器开火
        TankAI.hold_fire     停止射击
        TankAI.rotate_to     转到指定方向

    注意，在一次update函数调用中，tank的同一种状态如果发生多次变化，则以最后一次状态为准
    ./tank目录专用于存放坦克AI程序，系统会自从该目录导入坦克AI程序，请确保所有逻辑都放在一个文件中
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

    # 战场更新频率
    FRAMERATE = 0.1

    def __init__(self, in_queue, out_queue, battle_id, tank_id):
        self.battle_id = battle_id
        self.id = tank_id
        self.in_queue = in_queue
        self.out_queue = out_queue
        # action用于保存每次update坦克控制程序产生的指令
        # 指令示例：{'tank_id': 't20342','battle_id': 'b203402','weapon':2,'direction':2,'fire':'on','status':3}
        self.action = {'tank_id': self.id,
                       'battle_id': self.battle_id}

        self.on_start()
        while True:

            if not self.in_queue.empty():
                battleinfo = self.in_queue.get()
                print('[tankAI]收到<战场数据>:', battleinfo)
                # 找到哪个坦克是自己的坦克
                self.find_myself(battleinfo)
                # 执行坦克控制程序逻辑
                self.on_update(battleinfo)
            # 为action签名
            self.update_action('name', self.id)
            # 将本次update产生的指令放入输出队列
            self.out_queue.put(self.action)
            sleep(TankAI.FRAMERATE)

    def find_myself(self, battleinfo):
        """
        在服务器返回的战场信息中找到自己的坦克并保存至self.mytank中
        :param battleinfo:战场对象
        :return:
        """
        tanks = battleinfo.tanks
        for tank in tanks:
            if self.id == tank.id:
                self.mytank = tank
                break

    def on_start(self):
        """
        内置方法，用于子类继承实现坦克控制程序的初始化工作
        :return:
        """
        pass

    def on_update(self, battle):
        """
        内置方法，用于子类继承实现坦克控制程序的控制逻辑
        :param battle:
        :return:
        """
        pass

    def move(self, direction: int, velocity: int = 5):
        """
        内置方法，按照指定方向和速度移动（会一直移动直到调用stop方法，或者发生碰撞）
        :param direction:移动方向
        :param velocity:移动速度
        """
        self.update_action('status', self.STATUS_MOVING)
        self.update_action('direction', direction)

    def stop_move(self):
        """
        内置方法，立即停止移动
        :return:
        """
        self.update_action('status', self.STATUS_STOP)

    def fire(self, weapon):
        """
        内置方法，使用weapon持续射击（使用坦克当前朝向射击）
        :param weapon:武器类型
        :return:
        """
        self.update_action('weapon', weapon)
        self.update_action('fire', 'on')

    def hold_fire(self):
        """
        内置方法，立即停火
        :return:
        """
        self.update_action('fire', 'off')

    def rotate_to(self, direction):
        """
        内置方法，转向到direction这个方向
        :param direction:
        :return:
        """
        self.update_action('direction', direction)

    def update_action(self, type, value):
        self.action.update({type: value})
