# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 下午6:30
from server.tank.tank import *
from server.tank.battlefield import *
from server.tank.barrier import Barrier
from server.websocket_server import SimpleBroadServer, SimpleWebSocketServer
from multiprocessing import Queue, Process
from time import sleep, ctime
import os
import subprocess
from select import *
from socket import *

# 战场更新频率
FRAMERATE = 0.1
# webscoket服务器host
HOST = ''
# socket服务端口
PORT = 9000
# webscoket服务器端口
WEBSOCKET_PORT = 8000
# 观战网页文件的本地地址
WEBSOCKET_CLIENT_URL = '/client/websocket.html'


def mainloop(bt: Battlefield):
    q = Queue()
    # 通过websocket server对外提供战场信息更新
    websocket_p = Process(target=start_websocket_server, name='websocket', args=(q,))
    websocket_p.start()
    # 通过UDP和游戏客户端通信
    # p = Process(target=clientHandler(), name='socket', args=(q,))
    # p.start()

    while True:
        # 更新战场信息
        bt.update()
        # 存入要广播出去的战场信息
        q.put(bt)

        sleep(FRAMERATE)


def start_websocket_server(queue: Queue):
    SimpleBroadServer.queue = queue
    SimpleBroadServer.framerate = FRAMERATE
    server = SimpleWebSocketServer(HOST, WEBSOCKET_PORT, SimpleBroadServer)
    open_websocket_client(WEBSOCKET_CLIENT_URL)
    server.serveforever()


def open_websocket_client(url):
    print('打开本地浏览器')
    path = os.getcwd() + url
    subprocess.run(['chromium-browser', path])
    # os.system('chromium-browser ' + os.getcwd() + url + ' 2>/dev/null&')


class BattleManager:
    def __init__(self):
        self.battlefields = []

    def add_battlefield(self, bt: Battlefield):
        self.battlefields.append(bt)

    def remove_battlefield(self, bt: Battlefield):
        if len(self.battlefields):
            self.battlefields.remove(bt)


def main():
    bt = Battlefield(600, 400)
    # bt.add_barrier(Barrier(20, 10, 100, 100))
    # bt.add_barrier(Barrier(10, 15, 300, 500))
    t1 = Tank('t1')
    t1.set_position(50, 50)
    t1.set_status(Tank.STATUS_MOVING)
    t1.set_direction(Tank.DIRECTION_RIGHT)

    t2 = Tank('t2')
    t2.set_position(300, 50)
    t2.set_status(Tank.STATUS_MOVING)
    t2.set_direction(Tank.DIRECTION_LEFT)

    bt.add_tank(t1)
    bt.add_tank(t2)

    t1.fire(t1.weapon1)
    t2.fire(t2.weapon2)

    main_p = Process(target=mainloop, args=(bt,))
    main_p.start()
    main_p.join()


def clientHandler():
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(10)

    # 将关注的ＩＯ放入rlist
    rlist = [s]
    wlist = []
    xlist = [s]

    while True:
        # print("等待ＩＯ")
        # wlist中有内容select会立即返回
        rs, ws, xs = select(rlist, wlist, xlist)
        # msg = 'rs:%d ws:%d' % (len(rlist), len(wlist))
        # print(msg)
        for r in rs:
            # 表示套接字准备就绪
            if r is s:
                connfd, addr = r.accept()
                print("Connect from", addr)
                # 将新的套接字加入到关注列表
                rlist.append(connfd)
            else:
                try:
                    # 接收消息
                    data = r.recv(1024)
                    # 无数据或客户端用户名密码验证失败
                    if not data or not verify_user(data):
                        rlist.remove(r)
                        r.close()
                    else:
                        print("Received from", r.getpeername(), \
                              ":", data.decode())
                        # 想发消息可以放到写关注列表
                        wlist.append(r)
                except Exception:
                    pass

        for w in ws:
            # 发送信息
            w.send(str(ctime()).encode())
            wlist.remove(w)

        for x in xs:
            if x is s:
                s.close()
                sys.exit(1)


def verify_user(data):
    # 验证用户名密码
    return True


if __name__ == '__main__':
    main()
