# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 下午7:42
from server.tank.battlefield import Battlefield

"""
    encoder函数将战场信息提取出来并进行编码
    数据组间以分号分隔，属性间以冒号分隔

    例如：
    width:20|height:20|x:50|y:50|name:t1|life:100|oil:100|weapon:0|status:3|direction:2|velocity:5;
    width:20|height:20|x:300|y:50|name:t2|life:100|oil:100|weapon:0|status:3|direction:3|velocity:5;
    width:2|height:2|x:300|y:50|name:t2_1|status:3|direction:3|velocity:5;
"""


class InfoCoder():
    # 将需要过滤掉的属性名放入FILTER
    FILTER = ['socket_addr',
              'battlefield',
              'die_callback',
              'countdown']

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
