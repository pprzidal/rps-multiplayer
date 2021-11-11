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

    def _sendToBoth(self, message: str):
        self._a.send(Server._toUTF8(message))
        self._b.send(Server._toUTF8(message))

    def _toUTF8(self, txt: str):
        return f"{txt}\n".encode('UTF-8')

    def _send(self, wer: socket.socket, was: str):
        wer.send(Server._toUTF8(was))

    def waitForAnswer(self, socket: socket.socket):
        mes = socket.recv(1024).decode('UTF-8')
        if socket == self._a:
            self._aresp = mes
        else:
            self._bresp = mes

    def loop(self):
        self._a = self._socket.accept()
        # TODO \n maybe?
        Server._send(self._a, "Waiting for opponent")
        self._b = self._socket.accept()
        Server._sendToBoth(self._a, self._b, "We found an opponent for you")
        # TODO loop hier?
        while True:
            athread = threading.Thread(target=Server.waitForAnswer(), args=[self._a])
            bthread = threading.Thread(target=Server.waitForAnswer(), args=[self._b])
            athread.start()
            bthread.start()
            athread.join()
            bthread.join()
            ans = self.game.play(RockPaperScissors.toInt(self._aresp.lower()), RockPaperScissors.toInt(self._bresp.lower()))
            if ans == None:
                Server._sendToBoth("Tie!")
            elif ans == 'player':
                Server._send(self._a, "You won!")
                Server._send(self._b, "You lost!")
            elif ans == 'computer':
                Server._send(self._b, "You won!")
                Server._send(self._a, "You lost!")


if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except ValueError:
        print("man")
        sys.exit(1)
    Server(port).loop()