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


        battle─┬───width─────
               ├───height────
               ├───tanks─────┬───tank─┬───width
                                      ├───height
                                      ├───x
                                      ├───y
                                      ├───status
                                      ├───height
                                      ├───height
                                      ├───height


               ├───barriers──
               └───bullets───
        TankAI.move()
        TankAI.fire()
        TankAI.stop()
        TankAI.rotate()
    """

    def on_start(self):
        """
        内置初始化方法，系统只调用一次，可以用于在on_update前做一些准备工作
        :return:
        """
        self.name = 'tank1'
        self.move(self.DIRECTION_RIGHT, 5)

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
