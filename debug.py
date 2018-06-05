# coding:utf8
'''
author : Guoxi
email  : splinzer@gmail.com
time   : 2018 下午4:08
'''
import sys
from pathlib import Path

# 调试模式开关
# 打开时，所有print语句输出的文字前会自动加上所属.py文件名
# 关闭时，会屏蔽掉所有print输出
__debug_mode = True


def __debug(func):
    def wrapper(*args, **kw):
        filename = str(Path(sys.argv[0]).name) + ':'
        if __debug:
            return func(filename, *args, **kw)

    return wrapper


__p = print
print = __debug(__p)
