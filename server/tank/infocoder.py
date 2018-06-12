# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 下午7:42
from server.tank.battlefield import Battlefield

"""
    encoder函数将战场信息提取出来并进行编码
    数据组间以分号分隔，属性间以冒号分隔

    例如：
    name:t1|width:20|height:20|x:213|y:82|direction:4|velocity:5|type:tank|life:100|oil:100|weapon1:500|weapon2:500|status:3;
    name:t2|width:20|height:20|x:509|y:310|direction:4|velocity:5|type:tank|life:100|oil:100|weapon1:500|weapon2:500|status:3;
    name:b1|width:20|height:20|x:213|y:82|direction:4|velocity:5|type:bullet|status:3;
    name:b2|width:20|height:20|x:509|y:310|direction:4|velocity:5|type:bullet|status:3;
    name:r1|width:20|height:20|x:213|y:82|direction:4|velocity:5|type:barrier;
    name:r2|width:20|height:20|x:509|y:310|direction:4|velocity:5|type:barrier;
"""


class InfoCoder():
    # 将需要过滤掉的属性名放入FILTER
    FILTER = ['socket_addr',
              'battlefield',
              'die_callback',
              'countdown',
              'owner']

    def encoder(self, bt: Battlefield):
        ls = ''

        for i in bt.get_all_objects():
            for k, v in i.__dict__.items():
                if k not in self.FILTER:
                    s = k + ':' + str(v)
                    ls += s + '|'
            ls = ls[:-1]
            ls += ';'

        return ls[:-1]

    def encoder_tanks(self, bt: Battlefield):
        ls = ''

        for i in bt.get_tanks():
            for k, v in i.__dict__.items():
                if k not in self.FILTER:
                    s = k + ':' + str(v)
                    ls += s + '|'
            ls = ls[:-1]
            ls += ';'

        return ls[:-1]
