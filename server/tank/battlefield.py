# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 下午5:52
from server.tank.barrier import Barrier
from server.tank.rectobject import RectObject
from server.tank.tank import Tank
from server.tank.tank import *
from server.tank.point import Point
from multiprocessing import Process, Queue
from time import sleep


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
        super().__init__(width, height, Point(0, 0))
        self.tanks = []
        self.barriers = []

    def set_all_tanks(self):
        pass

    def fire(self, name, direction):
        pass

    def is_on_edge(self, _tank) -> bool:
        """
        检测所给坦克是否到达战场边沿
        :param _tank:坦克对象
        :return:布尔值，在战场边沿为True
        """
        pos = _tank.position
        width = _tank.width
        height = _tank.height

        if pos.x <= 0 or (pos.x + width) >= self.width or pos.y <= 0 or (pos.y + height) >= self.height:
            print('{}到达战场边沿'.format(_tank.name))
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
            if self.is_on_edge(_tank):
                _tank.stop()
            # 先将状态重置为正常，而后根据碰撞检测再修改设置
            # _tank.ready()
            for other_tank in self.tanks:
                if _tank != other_tank and self.isCollide(_tank, other_tank):
                    print('{}和{}发生碰撞'.format(_tank.name, other_tank.name))
                    _tank.stop()
                    other_tank.stop()

            for barrier in self.barriers:
                if self.isCollide(_tank, barrier):
                    _tank.stop()

    def add_barrier(self, barrier: Barrier) -> list:
        """
        向战场增加障碍物
        :param barrier:障碍物实例
        :return: 战场中所有障碍物的列表
        """
        self.barriers.append(barrier)
        return self.barriers

    def get_all_barrier(self) -> list:
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
        self.tanks.append(_tank)
        return self.tanks

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

    def get_all_tanks(self):
        """
        返回战场中所有的坦克
        :return: 坦克列表
        """
        return self.tanks

    def update_all_tanks(self):
        for i in self.tanks:
            i.update()

    # 计算并刷新数据
    def update(self):
        self.update_all_tanks()
        self.collision_stat_update()
