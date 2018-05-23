# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 下午7:47
from socket import *
import sys
import os
import signal
from time import sleep

# 子进程发送战斗指令

def do_child(s, name, addr):
    while True:
        sleep(0.5)
        text = 'MOVETO:UP&5|STOP|FIRE:2&LEFT'
        # 用户退出
        if text == "quit":
            msg = "Q " + name
            s.sendto(msg.encode(), addr)
            # 从子进程中杀掉父进程
            os.kill(os.getppid(), signal.SIGKILL)
            sys.exit("退出战斗")
        # 正常聊天
        else:
            s.sendto(text.encode(), addr)


# 父进程接收战场信息

def do_parent(s):
    while True:
        msg, addr = s.recvfrom(1024)
        print(msg.decode(), end="")


def main():
    if len(sys.argv) < 3:
        print("argv is error")
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST, PORT)

    s = socket(AF_INET, SOCK_DGRAM)

    while True:
        name = input("请输入姓名：")
        msg = 'L ' + name
        s.sendto(msg.encode(), ADDR)
        data, addr = s.recvfrom(1024)
        if data.decode() == 'OK':
            print("进入战场")
            break
        else:
            print(data.decode())

    pid = os.fork()
    if pid < 0:
        print("创建子进程失败")
    elif pid == 0:
        do_child(s, name, ADDR)
    else:
        do_parent(s)


if __name__ == "__main__":
    main()
