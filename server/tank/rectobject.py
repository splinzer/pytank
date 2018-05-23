# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 下午7:33
class RectObject():
    '''长方形物体类'''

    def __init__(self, width: int, height: int, position: tuple):
        '''
        初始化
        :param width: 宽度
        :param height: 高度
        :param position: 位置
        '''
        self.width = width
        self.height = height
        # 以左上角为坐标基准点
        self.position = position

    def set_position(self, x: int, y: int):
        '''
        设置位置
        :param x: x坐标
        :param y: y坐标
        :return: None
        '''
        self.position = x, y

    def get_position(self):
        '''
        返回坐标
        :return: 坐标(x,y)
        '''
        return self.position

    def isCollide(self, obj, other_obj):
        '''
        计算所有物体之间是否有位置重叠，有则视为发生碰撞
        :param obj:要检测的物体
        :param other_obj:要检测的物体
        :return: 布尔值，检测到碰撞返回True
        '''
        x1 = obj.position[0]
        y1 = obj.position[1]
        x2 = other_obj.position[0]
        y2 = other_obj.position[0]

        width = obj.width if x1 < x2 else other_obj.width
        height = obj.height if y1 < y2 else other_obj.height

        if abs(x1 - x2) <= width and abs(y1 - y2) <= height:
            return True
        else:
            return False