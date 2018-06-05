# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 下午7:42

from server.SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from server.tank.infocoder import InfoCoder
from threading import Thread
from time import sleep

HOST = ''
PORT = 8000

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
        print(f'[server]启动<websocket伺服>在<({HOST},{PORT})>')
        while True:
            data = self.queue.get()
            coder = InfoCoder()
            data = coder.encoder(data)
            self.sendMessage(data)
            sleep(self.framerate)


if __name__ == "__main__":
    server = SimpleWebSocketServer(HOST, PORT, SimpleBroadServer)
    server.serveforever()
