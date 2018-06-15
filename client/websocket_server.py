# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 下午7:42

from client.SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from threading import Thread
from time import sleep


class SimpleBroadServer(WebSocket):


    def handleMessage(self):
        pass
        # echo message back to client
        # self.sendMessage(self.data)

    def handleConnected(self):
        print(f'[websocket]已连接<{self.address}>')
        self.th = Thread(target=self.broadCast)
        self.th.start()

    def handleClose(self):
        print(self.address, 'closed')
        self.th.join()

    def broadCast(self):
        """
        从消息队列获取信息并通过websocket发出
        :return:
        """
        while True:
            data = self.queue.get()
            # coder = InfoCoder()
            # data = coder.encoder(data)
            self.sendMessage(data)
            sleep(0.05)
