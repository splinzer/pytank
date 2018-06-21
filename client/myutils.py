# coding:utf8
'''
author : Guoxi
email  : splinzer@gmail.com
time   : 2018/06/21 上午9:45
'''
from shutil import which


def which_app(namelist: list) -> dict:
    """
    根据所给的程序名称列表，返回当前系统可用的程序字典：键是程序名，值是路径
    :param namelist: 程序名称列表
    :return dict: 可用的程序名列表
    例如：
    which_app(['wget',
                    'curl',
                    'firefox',
                    'chromium-browser',
                    'explorer'])
    返回值为：   {'wget': '/usr/bin/wget',
                'curl': '/usr/bin/curl',
                'firefox': '/usr/bin/firefox',
                'chromium-browser': '/usr/bin/chromium-browser'}
    这说明系统上找不到名为explorer的程序
    """
    return {x: which(x) for x in namelist if which(x)}


if __name__ == '__main__':
    namelist = ['wget','curl','firefox','chromium-browser','explorer']
    print(list(which_app(namelist)))