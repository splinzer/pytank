# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 下午7:42
from server.tank.battlefield import Battlefield

"""
    encoder函数将战场信息提取出来并进行编码
    坦克属性编码的含义：
    NM：坦克名称
    PS：坦克位置
    WP：坦克武器
    AM：坦克弹药量
    ST：坦克状态
    DR：坦克方向
    
    例如：NM:T1|PS:200,100|WP:2|AM:500|ST:D;NM:T2|PS:100,100|WP:1|AM:600|ST:M;
"""
def encoder(bt: Battlefield):
    pass
    return 'NM:T1|PS:200,100|WP:2|AM:500|ST:D;NM:T2|PS:100,100|WP:1|AM:600|ST:M;\
    NM:T2|PS:200,100|WP:2|AM:500|ST:D;NM:T2|PS:100,100|WP:1|AM:600|ST:M'
