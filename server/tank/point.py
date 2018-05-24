# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 上午9:18


class Point():
    """
    坐标点类
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def getPoint(self):
        return self.x, self.y

    def setPoint(self, x: int, y: int):
        self.x = x
        self.y = y

