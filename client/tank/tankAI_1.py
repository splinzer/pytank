# coding:utf8
'''
author : Guoxi
email  : splinzer@gmail.com
time   : 2018 下午2:08
'''
from client.tankAI import *
from random import randint


class AI(TankAI):
    """
    AI类用于控制坦克的移动、攻击，你应该在这个类里实现所有坦克的控制逻辑

    - on_update方法的第二个参数battle对象专门用于获取战场信息，该对象结构如下：

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

        start_move    向指定方向持续移动
        stop_move     停止移动
        start_fire    使用指定武器开火
        hold_fire     停止射击

    - 状态：坦克
        STATUS_DEAD 死亡状态，该状态的物体无法移动，且状态不再发生变化
        STATUS_STOP 停止状态，除非状态被重置其他状态，否则物体会一直保持静止不动
        STATUS_MOVING 移动中状态，除非碰撞到物体或边界，该状态的物体会一直按照其方向移动

    注意，在一次update函数调用中，tank的同一种状态如果发生多次变化，则以最后一次状态为准
    ./tank目录专用于存放坦克AI程序，系统会自从该目录导入坦克AI程序，请确保所有逻辑都放在一个文件中
    """

    def on_start(self):
        """
        内置初始化方法，系统只调用一次，可以用于在on_update前做一些准备工作
        :return:
        """
        # 通过以下方式设置坦克的名字，这个名字会显示到战场上（如不设置，坦克默认名字是”无名氏“）
        self.action.update({'name': 'tom'})
        # 向右侧移动
        self.start_move(self.DIRECTION_RIGHT)

    def on_update(self, battle):
        """
        内置方法，该方法会被循环调用，请在该方法中实现tank的控制逻辑
        :param battle: 战场对象，通过该对象可以获得关于战场的一切信息，包括：所有坦克、障碍物、子弹的数据
        :return: 无
        """
        tanks = battle.tanks
        barriers = battle.barriers
        bullets = battle.bullets

        # print('tankAI_1:', tanks)
        # print('tankAI_1:', tanks[0])

        self.random_move(battle)
        self.random_fire()
        # for tank in tanks:
        #     # 如探测到敌方坦克进入攻击范围，发起攻击
        #     direction = self.is_nearby(tank)
        #     if direction and tank == self.mytank:
        #         self.fire(weapon=self.WEAPON_1)
        #
        # for barrier in barriers:
        #     # 蔽开障碍物
        #     pass
        #
        # for bullet in bullets:
        #     # 躲避子弹
        #     pass

    # 反弹
    def is_nearby(self, tank):
        """
        示例方法：用于判断敌方坦克与我方坦克在x轴或y轴上是否比较接近
        :param tank: 敌方坦克对象
        :return: 发现满足条件的敌方坦克，则返回敌方坦克的方位，否则返回False
        """
        direction = self.DIRECTION_RIGHT
        if abs(self.mytank.x - tank.x) < 10 or abs(self.mytank.y - tank.y) < 10:
            # 判断敌方坦克位于我方坦克的方位
            if tank.x >= self.mytank.x:
                direction = self.DIRECTION_RIGHT
            elif tank.x < self.mytank.x:
                direction = self.DIRECTION_LEFT
            elif tank.y >= self.mytank.y:
                direction = self.DIRECTION_DOWN
            elif tank.y < self.mytank.y:
                direction = self.DIRECTION_UP
            return direction
        else:
            return False
