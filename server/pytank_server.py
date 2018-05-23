# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 下午6:30

from socket import *
from multiprocessing import Process
import sys
import os


# 实现登录


def do_login(s, user, name, addr):
    if (name in user) or name == "管理员":
        s.sendto("该用户已存在，请重新输入".encode(), addr)
        return

    s.sendto(b'OK', addr)
    msg = "\n %s 进入战场" % name
    # 通知所有人
    for i in user:
        s.sendto(msg.encode(), user[i])
    # 将用户插入字典
    user[name] = addr
    return


def do_chat(s, user, cmd):
    # cmd = ['C','zhang','I','love','China']
    msg = "\n%-4s: %s" % (cmd[1], ' '.join(cmd[2:]))

    # 发送给所有人，除了自己
    for i in user:
        if i != cmd[1]:
            s.sendto(msg.encode(), user[i])
    return


def do_quit(s, user, name):
    del user[name]
    msg = "\n" + name + "离开了聊天室"
    for i in user:
        s.sendto(msg.encode(), user[i])
    return


# 子进程处理客户端指令

def command_handler(s):
    # 字典用来存储用户信息 {name:(ip,port)}
    user = {}
    # 循环接受请求
    while True:
        msg, addr = s.recvfrom(1024)
        msg = msg.decode()
        # 解析客户端指令
        cmd = msg.split('|')
        cmdandpara = {}
        for i in cmd:
            keyandvalue = i.split(':')
            if len(keyandvalue) == 2:
                cmdandpara[keyandvalue[0]] = tuple(keyandvalue[1].split('&'))
            else:
                cmdandpara[i] = ()
        # # 根据不同请求做不同事情
        # if cmd[0] == 'L':
        #     do_login(s, user, cmd[1], addr)
        # elif cmd[0] == 'C':
        #     do_chat(s, user, cmd)
        # elif cmd[0] == 'Q':
        #     do_quit(s, user, cmd[1])
        # else:
        #     s.sendto("请求错误".encode(), addr)


# 广播战场消息
def do_parent(s, addr):
    while True:
        msg = input("管理员消息：")
        msg = "C 管理员 " + msg
        s.sendto(msg.encode(), addr)
    s.close()
    sys.exit(0)


def main():
    HOST = '127.0.0.1'
    PORT = 9999
    ADDR = (HOST, PORT)

    # 使用数据报套接字
    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)

    # 创建子进程
    # 用于接收客户端指令的进程
    command_ps = Process(name='command_ps', target=command_handler)
    # 用于向客户端广播消息的进程
    broadcast_ps = Process(name='broadcast_ps', target=None)
    # 用于计算和更新战场数据的进程
    battlefield_ps = Process(name='battlefield_ps', target=None)
    # 用于向UI界面提供websocket接口的进程
    websocket_ps = Process(name='websocket_ps', target=None)


if __name__ == "__main__":
    main()
