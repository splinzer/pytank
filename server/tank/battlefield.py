# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 下午5:52
from server.tank.barrier import Barrier
from server.tank.rectobject import RectObject
from server.tank.tank import Tank
from server.tank.tank import *


class Battlefield(RectObject):
    """
    战场类
    用于计算和保存所有战场战况相关的数据
    """

    def __init__(self, width: int, height: int):
        """
        战场类构造函数
        :param width:战场宽度
        :param height: 战场高度
        """
        super().__init__(width, height, 0, 0)
        self.type = 'battlefield'
        self.tanks = []
        self.barriers = []
        self.bullets = []

    def is_on_edge(self, _tank: RectObject) -> bool:
        """
        检测所给坦克是否到达战场边沿
        :param _tank:坦克对象
        :return:布尔值，在战场边沿为True
        """
        # import pdb;pdb.set_trace()
        pos = _tank.get_position()
        x = pos[0]
        y = pos[1]
        width = _tank.width
        height = _tank.height

        if x <= 0 or (x + width) >= self.width or y <= 0 or (y + height) >= self.height:
            # print('{}到达战场边沿'.format(_tank.name))
            return True
        return False

    def collision_stat_update(self):
        """
        更新所有坦克的碰撞状态
        :return:None
        我们有以下几个检测碰撞的策略：
        1.整体计算移动前预测是否会发生碰撞，如果会发生碰撞，相关物体停止移动。
        2.整体计算每移动一步后检测是否已经发生了碰撞，如果发生碰撞，相关物体停止移动。（可能存在物体位置交叠的情况，需要重置位置）
        3.每个坦克自己每一次移动前预测是否会发生碰撞，如果会发生，则停止
        """
        for _tank in self.tanks:

            # 坦克达到战场边界停止移动
            if self.is_on_edge(_tank):
                print('tank:{}抵达边界停止'.format(_tank))
                _tank.stop()

            # 先将状态重置为正常，而后根据碰撞检测再修改设置
            # _tank.ready()
            for other_tank in self.tanks:
                if _tank != other_tank and self.isCollide(_tank, other_tank):
                    # print('{}和{}发生碰撞'.format(_tank.name, other_tank.name))
                    _tank.stop()
                    other_tank.stop()

            for barrier in self.barriers:
                if self.isCollide(_tank, barrier):
                    # print('tank:{}碰到障碍物停止'.format(_tank))
                    _tank.stop()

        # 当子弹到达战场边界自毁
        for _bullet in self.bullets:
            if self.is_on_edge(_bullet):
                print('子弹：{}抵达边界销毁'.format(_bullet))
                # self.bullets.remove(_bullet)
                _bullet.die(self.remove_object)

    def add_barrier(self, barrier: Barrier) -> list:
        """
        向战场增加障碍物
        :param barrier:障碍物实例
        :return: 战场中所有障碍物的列表
        """
        self.barriers.append(barrier)
        return self.barriers

    def get_barriers(self) -> list:
        """
        返回战场中所有的障碍物
        :return: 障碍物实例列表
        """
        return self.barriers

    def add_tank(self, _tank: Tank) -> list:
        """
        向战场增加坦克
        :param _tank:坦克实例
        :return: 战场中所有坦克的列表
        """
        # _tank.set_position(self.get_random_position(_tank))
        _tank.set_battlefield(self)
        self.tanks.append(_tank)
        return self.tanks

    def add_bullet(self, _bullet: Bullet):
        self.bullets.append(_bullet)

    def get_bullets(self):
        return self.bullets

    def remove_object(self, rectObject: RectObject):
        print('bullets:', len(self.bullets))
        if rectObject in self.bullets:
            self.bullets.remove(rectObject)
            print('bullets:', len(self.bullets))

    def get_random_position(self, _object):
        """
        返回一个随机的且不发生碰撞的位置，会根据要放置的物体_object的尺寸计算
        :param _object: 物体
        :return:
        """

        for _tank in self.tanks:
            if self.isCollide(_tank, _object):
                return

        for barrier in self.barriers:
            if self.isCollide(barrier, _object):
                return

    def get_tanks(self):
        """
        返回战场中所有的坦克
        :return: 坦克列表
        """
        return self.tanks

    def get_all_objects(self):
        return self.get_tanks() + self.get_bullets()

    def update_tanks(self):
        for _tank in self.tanks:
            _tank.update()

    def update_bullets(self):
        for _bullet in self.bullets:
            _bullet.update()

    # 计算并刷新数据
    def update(self, str=None):
        """
        根据客户端传回的指令更新战场
        :param str:客户端指令
        :return:
        """
        # 先根据客户端传回的指令更新战场
        if str:
            print('战场收到客户端指令', str)
            # TODO 指令解码并据此更新战场

            pass
        self.update_tanks()
        self.update_bullets()
        self.collision_stat_update()
