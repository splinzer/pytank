# coding:utf8
'''
author : Guoxi
email  : splinzer@gmail.com
time   : 2018 下午6:38
'''
from client.battle import Battle


class Coder:
    # todo 这里的编码和解码方式可以其使用json方式替代
    @classmethod
    def getBattleClass(cls, s):
        """
        用于把服务器传来的战场信息字符串转成一个类对象，以方便通过.操作符访问
        :param s:如下形式的字符串：
        name:t1|width:20|height:20|x:65|y:50|direction:4|velocity:5|type:tank|life:100|oil:100|weapon1:500|weapon2:500|status:4;
        name:t2|width:20|height:20|x:285|y:50|direction:3|velocity:5|type:tank|life:100|oil:100|weapon1:500|weapon2:500|status:4;
        name:t1_1|width:4|height:4|x:90|y:60|direction:4|velocity:10|type:bullet|weapon_type:500|status:4;
        name:t2_2|width:4|height:4|x:280|y:60|direction:3|velocity:10|type:bullet|weapon_type:500|status:4
        :return:返回一个Battle对象，可以使用battle.tanks[0].width的形式访问坦克的属性
        """
        tanks = []
        bullets = []
        barriers = []
        battlefied = None
        for i in cls.__transfer(s):
            if i['type'] == 'tank':
                tanks.append(dict_to_class(i))
            elif i['type'] == 'bullet':
                bullets.append(dict_to_class(i))
            elif i['type'] == 'barrier':
                barriers.append(dict_to_class(i))
            elif i['type'] == 'battlefield':
                battlefied = dict_to_class(i)

        return Battle(tanks, bullets, barriers, battlefied)

    @classmethod
    def __transfer(self, s):
        """
        用于把服务器传来的战场信息字符串转成对象列表（从第1种形式转成第2种形式）
        第1种形式：
        name:t1|width:20|height:20|x:65|y:50|direction:4|velocity:5|type:tank|life:100|oil:100|weapon1:500|weapon2:500|status:4;
        name:t2|width:20|height:20|x:285|y:50|direction:3|velocity:5|type:tank|life:100|oil:100|weapon1:500|weapon2:500|status:4;
        name:t1_1|width:4|height:4|x:90|y:60|direction:4|velocity:10|type:bullet|weapon_type:500|status:4;
        name:t2_2|width:4|height:4|x:280|y:60|direction:3|velocity:10|type:bullet|weapon_type:500|status:4
        第2种形式：
        [{name:t1,width:20...},{name:t2,width:20...}]

        :return: 返回第2种形式的列表
        """
        ds = []
        objs = s.split(';')
        for obj in objs:
            d = {}
            obj = obj.split('|')
            for item in obj:
                item = item.split(':')
                try:
                    d[item[0]] = int(item[1])
                except Exception:
                    d[item[0]] = item[1]
            ds.append(d)
        return ds


class dict_to_class(object):
    """
    用于把一个dict转成class，这样便于采用object.attribute的方式访问
    """

    def __init__(self, o: dict):
        for k, v in o.items():
            setattr(self, k, v)

    def __getattribute__(self, attr):
        return super().__getattribute__(attr)

    def __getitem__(self, attr):
        return super().__getattribute__(attr)
