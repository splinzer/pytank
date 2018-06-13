# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 下午5:52
from server.tank.barrier import Barrier
from server.tank.tank import *
import json


class Battlefield(BattleObject):
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
        # 标识战斗是否结束
        self.gameover = False
        # 用于标识战斗结束消息是否已经发给客户端了
        self.gameover_sended = False

    def game_over(self):
        self.gameover = True
        # todo 需要从共享列表中清除已经结束的战斗

    def collision_stat_update(self):
        """
        更新所有坦克的碰撞状态
        todo 碰撞检测算法需要优化，目前采用全排列方式效率太低
        :return:None
        """
        # 获取所有战场对象
        all_objects = self.get_all_objects()
        for one_object in all_objects:
            for other_object in all_objects:
                if other_object != one_object and self.is_collide(one_object, other_object):
                    # 坦克相撞停止
                    if other_object.type == 'tank' and one_object.type == 'tank':
                        one_object.stop()
                        other_object.stop()
                    # 坦克与子弹相撞子弹销毁，坦克减血，子弹销毁
                    elif other_object.type == 'bullet' \
                            and one_object.type == 'tank' \
                            and other_object.owner != one_object:
                        # 减去1点血
                        one_object.loss_life(20)
                        other_object.suicide()

    def get_all_objects(self):
        """返回所有战场对象"""
        return self.get_tanks() + self.get_bullets() + self.get_bullets()

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

    def remove_object(self, rectObject: BattleObject):
        target = []
        if rectObject.type == 'tank':
            target = self.tanks
        elif rectObject.type == 'bullet':
            target = self.bullets
        target.remove(rectObject)

    def get_random_position(self, _object):
        """
        返回一个随机的且不发生碰撞的位置，会根据要放置的物体_object的尺寸计算
        :param _object: 物体
        :return:
        """

        for _tank in self.tanks:
            if self.is_collide(_tank, _object):
                return

        for barrier in self.barriers:
            if self.is_collide(barrier, _object):
                return

    def get_tanks(self):
        """
        返回战场中所有的坦克
        :return: 坦克列表
        """
        return self.tanks

    def update_tanks(self):
        for _tank in self.tanks:
            _tank.update()

    def update_bullets(self):
        for _bullet in self.bullets:
            _bullet.update()

    # 计算并刷新数据
    def update_before_send(self, tankinfo=None):
        """
        根据客户端传回的指令更新战场
        :param tankinfo:坦克信息对象，如：{'battle_id':'b20340','id':'t20394','weapon':2,'direction':2,'fire':'on','status':3}
        :return:
        """
        # 判断战斗是否结束：只剩一个坦克或没有坦克
        if len(self.tanks) <= 1:
            self.game_over()
            
        # 先根据客户端传回的指令更新战场
        if tankinfo:
            tank_id = tankinfo['id']
            # 当前版本每次只能接收一个坦克的更新信息，所有每次只更新一个坦克
            for tank in self.tanks:
                if tank.id == tank_id:
                    # 客户端启动之初可能会有不完整的指令发来，字段使用前需要检测是否可用
                    if 'direction' in tankinfo.keys():
                        tank.set_direction(tankinfo['direction'])
                    if 'status' in tankinfo.keys():
                        tank.set_status(tankinfo['status'])
                    if tankinfo.get('fire', None) == 'on':
                        tank.fire()

        # 客户端无指令时，也需要运算更新
        self.update_tanks()
        self.update_bullets()
        self.collision_stat_update()
