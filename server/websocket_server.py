# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 下午7:42

from server.SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from server.tank.infocoder import InfoCoder
from threading import Thread
from time import sleep


class SimpleBroadServer(WebSocket):

    def handleMessage(self):
        pass

    # echo message back to client
    # self.sendMessage(self.data)

    def handleConnected(self):
        print(self.address, 'connected')
        self.th = Thread(target=self.broadCast)
        self.th.start()

    def handleClose(self):
        print(self.address, 'closed')
        self.th.join()

    def broadCast(self):
        print('开始接收广播')
        while True:
            data = self.queue.get()
            coder = InfoCoder()
            data = coder.encoder(data)
            self.sendMessage(data)
            sleep(1)


if __name__ == "__main__":
    server = SimpleWebSocketServer('', 8000, SimpleBroadServer)
    server.serveforever()
