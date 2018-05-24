# websocket_server.py

from server.SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from time import sleep

class SimpleBroadServer(WebSocket):

    def handleMessage(self):
        pass

    # echo message back to client
    # self.sendMessage(self.data)

    def handleConnected(self):
        print(self.address, 'connected')
        while True:
            self.sendMessage('helllo')
            sleep(1)


    def handleClose(self):
        print(self.address, 'closed')

    def setMessageQueue(self, q):
        self.queue = q


if __name__ == "__main__":
    server = SimpleWebSocketServer('', 8000, SimpleBroadServer)
    server.serveforever()
