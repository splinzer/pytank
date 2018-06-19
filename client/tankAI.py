# coding:utf8
'''
author : Guoxi
email  : splinzer@gmail.com
time   : 2018 下午3:37
'''

# from multiprocessing import Connection
from time import sleep
from random import randint


class TankAI():
    """
    该类作为坦克控制类的超类，封装了一些底层方法，并提供了以下属性和方法便于编写控制逻辑

    - update方法的第二个参数battle对象专门用于获取战场信息，该对象结构如下：

        battle─┬───width（战场宽度）
               │
               ├───height（战场高度）
               │
               │
               │ （坦克对象列表）
               ├───tanks─────┬───tank─┬───id（唯一编号）
               │                      ├───type（物体类型，共2种：tank、bullet）
               │                      ├───width（坦克高度）
               │                      ├───height（坦克高度）
               │                      ├───x（x坐标）
               │                      ├───y（y坐标）
               │                      ├───status（当前状态，共3种：STATUS_DEAD、STATUS_STOP、STATUS_MOVING）
               │                      ├───block（为True表示当前被阻挡了，可能碰到了障碍物或碰到了战场边界）
               │                      ├───life（剩余血量）
               │                      ├───ammo(剩余弹药）
               │                      ├───oil（剩余油量）
               │
               │  （子弹对象列表）
               ├───bullets───┬───tank─┬───id（唯一编号）
               │                      ├───type（物体类型，共2种：tank、bullet）
               │                      ├───x（x坐标）
               │                      ├───y（y坐标）
               │                      ├───owner_id（发射该子弹的坦克id）
               └


    - 方法：提供了以下方法用于控制坦克进行战斗（详见方法注释）：

        self.start_move    向指定方向持续移动
        self.stop_move     停止移动
        self.start_fire    使用指定武器开火
        self.hold_fire     停止射击

    - 状态：坦克
        STATUS_DEAD 死亡状态，该状态的物体无法移动，且状态不再发生变化
        STATUS_STOP 停止状态，除非状态被重置其他状态，否则物体会一直保持静止不动
        STATUS_MOVING 移动中状态，除非碰撞到物体或边界，该状态的物体会一直按照其方向移动

    注意，在一次update函数调用中，tank的同一种状态如果发生多次变化，则以最后一次状态为准
    ./tank目录专用于存放坦克AI程序，系统会自从该目录导入坦克AI程序，请确保所有逻辑都放在一个文件中

    """


    STATUS_DEAD = 2
    STATUS_STOP = 3
    STATUS_MOVING = 4

    DIRECTION_UP = 1
    DIRECTION_DOWN = 2
    DIRECTION_LEFT = 3
    DIRECTION_RIGHT = 4

    # 战场更新频率
    FRAMERATE = 0.1

    def __init__(self, in_queue, out_queue, battle_id, tank_id):
        print('[tankAI]启动')
        self.name = '无名氏'
        self.battle_id = battle_id
        self.id = tank_id
        self.in_queue = in_queue
        self.out_queue = out_queue
        # 这里通过tank_id和battle_id为action签名，以便在服务端识别
        # 指令示例：{'id': 't20342','battle_id': 'b203402','weapon':2,'direction':2,'fire':'on','status':3}
        self.action = {'id': self.id,
                       'battle_id': self.battle_id,
                       'name':self.name}
        last_action = self.action.copy()
        self.on_start()
        while True:

            if not self.in_queue.empty():
                battleinfo = self.in_queue.get()
                # 找到哪个坦克是自己的坦克
                self.find_myself(battleinfo)
                # 执行坦克控制程序逻辑
                self.on_update(battleinfo)
            # self.update_action('name', self.id)
            # 程序运行之初self.action有可能为空
            if self.action:
                if last_action != self.action:
                    print('action',self.action)
                    # 将本次update产生的指令放入输出队列
                    self.out_queue.put(self.action)
                    # 记录本次action
                    last_action = self.action.copy()

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

    def start_move(self, direction: int, velocity: int = 5):
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

    def start_fire(self):
        """
        内置方法，使用weapon持续射击（使用坦克当前朝向射击）
        :param weapon:武器类型
        :return:
        """
        self.update_action('fire', 'on')

    def hold_fire(self):
        """
        内置方法，立即停火
        :return:
        """
        self.update_action('fire', 'off')

    def turn_to(self, direction):
        """
        内置方法，转向到direction这个方向
        :param direction:
        :return:
        """
        self.update_action('direction', direction)

    def random_fire(self):
        n = randint(0,5)
        if n == 5:
            self.start_fire()
        else:
            self.hold_fire()


    def void_edge(self, battle, delta=7):
        """
        根据提供的阈值来检测是否靠近战场边界，返回不会发生碰撞的方向
        :param battle: 战场信息对象
        :param delta: 定义触发阈值，如果坦克距离边界小于该值则触发
        :return: 集合对象，可用的方向
        """
        # 是否靠近边界默认值
        flag = False
        x = self.mytank.x
        y = self.mytank.y
        width = self.mytank.width
        height = self.mytank.height
        # 定义触发阈值，如果坦克距离边界小于该值则触发
        delta = 7
        # n_x和n_y是发生碰到边界时反弹后物体的新坐标
        n_x = x
        n_y = y

        directions = {self.DIRECTION_DOWN,
                      self.DIRECTION_UP,
                      self.DIRECTION_LEFT,
                      self.DIRECTION_RIGHT}
        # 靠近左侧边界
        if x <= width / 2 + delta:
            flag = True
            directions = directions - {self.DIRECTION_LEFT}
        # 靠近右侧边界
        print(x + width / 2 + delta,battle.width)
        if (x + width / 2 + delta) >= battle.width:
            flag = True
            directions = directions - {self.DIRECTION_RIGHT}
        # 靠近上边界
        if y <= height / 2 + delta:
            flag = True
            directions = directions - {self.DIRECTION_UP}
        # 靠近下边界
        if (y + height / 2 + delta) >= battle.height:
            flag = True
            directions = directions - {self.DIRECTION_DOWN}


        return flag, directions

    def random_turn(self, directions: set):
        """
        内置方法：让坦克随机转弯
        :return:
        """
        directions = list(directions)
        n = randint(0, len(directions) - 1)

        direction = directions[n]

        self.turn_to(direction)

    def random_move(self, battle):
        near_edge, avai_direct = self.void_edge(battle)
        if near_edge:
            self.random_turn(avai_direct)
        else:
            pass
            # if randint(0,10) == 5:
            #     self.random_turn(avai_direct)

    def update_action(self, type, value):
        self.action.update({type: value})
