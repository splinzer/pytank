# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 下午5:52
from .barrier import Barrier
from .rectobject import RectObject
from .tank import Tank


class Battlefield(RectObject):
    '''
    战场类
    用于计算和保存所有战场战况相关的数据
    '''

    def __init__(self, width: int, height: int):
        '''
        战场类构造函数
        :param width:战场宽度
        :param height: 战场高度
        '''
        super().__init__(width, height, (0, 0))
        self.tanks = []
        self.barriers = []

    def move(self, name: Tank, direction: str):
        '''
        让指定坦克朝指定方向持续移动
        :param name: 坦克名称
        :param direction: 移动方向，可选值为up,down,left,right
        :return: None
        '''
        positon = name.get_position()
        # 对移出战场范围的情况做处理
        if positon[0] >= self.width:
            name.set_position(self.width - 1, positon[1])

        if positon[1] >= self.height:
            name.set_position(positon[0], self.height - 1)

    def stop(self):
        pass

    def fire(selfs, name, direction):
        pass

    def collision_stat_update(self):
        '''
        更新所有坦克的碰撞状态
        :return:None
        '''
        for _tank in self.tanks:
            # 先将状态重置为正常，而后根据碰撞检测再修改设置
            _tank.set_status(Tank.STATUS_OK)
            for other_tank in self.tanks:
                if _tank != other_tank and self.isCollide(_tank, other_tank):
                    _tank.set_status(Tank.STATUS_STOP)
                    other_tank.set_status(Tank.STATUS_STOP)

            for barrier in self.barriers:
                if self.isCollide(_tank, barrier):
                    _tank.set_status(Tank.STATUS_STOP)

    def add_barrier(self, barrier: Barrier) -> list:
        '''
        向战场增加障碍物
        :param barrier:障碍物实例
        :return: 战场中所有障碍物的列表
        '''
        self.barriers.append(barrier)
        return self.barriers

    def get_all_barrier(self) -> list:
        '''
        返回战场中所有的障碍物
        :return: 障碍物实例列表
        '''
        return self.barriers

    def add_tank(self, _tank: Tank) -> list:
        '''
        向战场增加坦克
        :param _tank:坦克实例
        :return: 战场中所有坦克的列表
        '''
        # _tank.set_position(self.get_random_position(_tank))
        self.tanks.append(_tank)
        return self.tanks

    def get_random_position(self, _object):
        '''
        返回一个随机的且不发生碰撞的位置，会根据要放置的物体_object的尺寸计算
        :param _object: 物体
        :return:
        '''

        for _tank in self.tanks:
            if self.isCollide(_tank, _object):
                return

        for barrier in self.barriers:
            if self.isCollide(barrier, _object):
                return

    def get_all_tanks(self):
        '''
        返回战场中所有的坦克
        :return: 坦克列表
        '''
        return self.tanks


# 计算并刷新数据
def update(self):
    pass


def main():
    bt = Battlefield(600, 400)
    bt.add_barrier(Barrier(20, 10, (100, 100)))
    bt.add_barrier(Barrier(10, 15, (300, 500)))
    bt.add_tank(Tank('t1', ('127.0.0.1', 7777)))
    bt.add_tank(Tank('t2', ('127.0.0.1', 7778)))


if __name__ == '__main__':
    main()
