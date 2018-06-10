# coding:utf8
'''
author : Guoxi
email  : splinzer@gmail.com
time   : 2018 下午6:41
'''


class Battle():
    def __init__(self, tanks: list, bullets: list, barriers:list):
        self.tanks = tanks
        self.bullets = bullets
        self.barriers = barriers
        self.mytank = None
        self.width = 800
        self.height = 600
