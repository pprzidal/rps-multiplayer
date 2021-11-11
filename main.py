import socket, sys, threading
from game import RockPaperScissors


class Server:
    def __init__(self, port: int):
        self._socket = socket.socket()
        self._socket.bind(('', port))
        self._socket.listen(2)
        self._aresp, self._bresp = None, None
        self._a, self._b = None, None
        self.game = RockPaperScissors()
        self._disconnected = None

    def _sendToBoth(self, message: str):
        self._a.send(Server._toUTF8(message))
        self._b.send(Server._toUTF8(message))

    def _toUTF8(self, txt: str):
        return f"{txt}\n".encode('UTF-8')

    def _send(self, wer: socket.socket, was: str):
        wer.send(Server._toUTF8(was))

    def waitForAnswer(self, socket: socket.socket):
        text = ""
        while not text.contains("\n"):
            text = text + socket.recv(1024).decode('UTF-8')
        print(text)
        if text == "disconnect":
            self._disconnected = socket
        else:
            if socket == self._a:
                self._aresp = text
            else:
                self._bresp = text

    def loop(self):
        self._a = self._socket.accept()
        # TODO \n maybe?
        Server._send(self._a, "waiting")
        self._b = self._socket.accept()
        Server._sendToBoth(self._a, self._b, "found")
        while self._disconnected == None:
            athread = threading.Thread(target=Server.waitForAnswer(), args=[self._a])
            bthread = threading.Thread(target=Server.waitForAnswer(), args=[self._b])
            athread.start()
            bthread.start()
            athread.join()
            bthread.join()
            if self._disconnected != None:
                if self._disconnected == self._a:
                    Server._send(self._b, "disconnect")
                else:
                    Server._send(self._a, "disconnect")
                break
                

            ans = self.game.play(RockPaperScissors.toInt(self._aresp.lower()), RockPaperScissors.toInt(self._bresp.lower()))
            if ans == None:
                Server._send(self._a, f"tie;{self._bresp}")
                Server._send(self._b, f"tie;{self._aresp}")
            elif ans == 'player':
                Server._send(self._a, f"won;{self._bresp}")
                Server._send(self._b, f"lost;{self._aresp}")
            elif ans == 'computer':
                Server._send(self._b, f"won;{self._aresp}")
                Server._send(self._a, f"lost;{self._aresp}")


if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except ValueError:
        print("man")
        sys.exit(1)
    while True:
        Server(port).loop()