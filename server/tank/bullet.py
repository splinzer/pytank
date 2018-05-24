# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 上午8:56
from server.tank.rectobject import RectObject


class Bullet(RectObject):
    """
    子弹类
    """
    WEAPON_HEAVY = 0
    WEAPON_LIGHT = 1
    WEAPON_HEAVY_ATTAK = 10
    WEAPON_LIGHT_ATTAK = 5
    def __init__(self, weapon_type: int, position: tuple):
        super().__init__(width=2, height=2, position=position)
        self.weapon_type = weapon_type
