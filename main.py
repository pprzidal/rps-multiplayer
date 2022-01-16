import socket, sys, threading
from game import RockPaperScissors


class Server:
    def __init__(self, ip: str, port: int):
        self._socket = socket.socket()
        self._socket.bind((ip, port))  # Ever changing IP Address
        self._socket.listen()
        self._aresp = None
        self._bresp = None
        self._a = None
        self._b = None
        self.game = RockPaperScissors()
        self._disconnected = None

    def _sendToBoth(self, message: str):
        self._a.send(self._toUTF8(message))
        self._b.send(self._toUTF8(message))

    def _toUTF8(self, txt: str):
        return f"{txt}\n".encode('UTF-8')  # probably remove \n

    def _send(self, wer: socket.socket, was: str):
        wer.send(self._toUTF8(was))

    def waitForAnswer(self, socket: socket.socket):
        text = ""
        while "\n" not in text:
            text = text + socket.recv(1024).decode('UTF-8')
        text = text.strip()
        print("RECEIVED: " + text)
        if text == "disconnect":
            self._disconnected = socket
        else:
            if socket == self._a:
                self._aresp = text
            else:
                self._bresp = text

    def loop(self):
        print("--- Server Started")
        self._a, _info = self._socket.accept()
        print("--- First Client Found")
        self._send(self._a, "waiting")
        self._b, _info = self._socket.accept()
        print("--- Second Client Found")
        self._sendToBoth("found")
        while self._disconnected == None:  # Probably useless
            athread = threading.Thread(target=self.waitForAnswer, args=[self._a])
            bthread = threading.Thread(target=self.waitForAnswer, args=[self._b])
            athread.start()
            bthread.start()
            athread.join()
            bthread.join()

            if self._disconnected != None:
                if self._disconnected == self._a:
                    self._send(self._b, "disconnect")
                    self._a.close()
                else:
                    self._send(self._a, "disconnect")
                    self._b.close()
                print("--- Client Disconnected")
                break

            print("ARESP: " + self._aresp)
            print("BRESP: " + self._bresp)
            ans = self.game.play(self.game.toInt(self._aresp.lower()), dchoice=self.game.toInt(self._bresp.lower()))
            # print("WINNER IS: " + ans)
            if ans == None:
                self._send(self._a, f"tie;{self._bresp}")
                self._send(self._b, f"tie;{self._aresp}")
                print("WINNER IS: NO ONE")
            elif ans == 'player':
                self._send(self._a, f"won;{self._bresp}")
                self._send(self._b, f"lost;{self._aresp}")
                print("WINNER IS: " + "Spieler 1")
            elif ans == 'computer':
                self._send(self._b, f"won;{self._aresp}")
                self._send(self._a, f"lost;{self._aresp}")
                print("WINNER IS: " + "Spieler 2")


if __name__ == "__main__":
    try:
        port = int(sys.argv[2])
        ip = sys.argv[1]
    except Exception:
        print('Usage works like this: python main.py <ip> <port>\nport has to be a parsable int')
    else:
        while True:
            Server(ip, port).loop()