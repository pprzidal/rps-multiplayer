import socket
import threading


class Model:
    """
    Kümmert sich um die Verbindung zum GameServer und gibt diesem die Eingabe des Benutzers
    und schickt diesem Meldungen des Servers.
    """

    def __init__(self):
        self.p1Points = 0
        self.p2Points = 0
        self.rounds = 0
        self.p2Choice = None
        self.message = None
        self.s = None
        self.status = 0

    def reset(self):
        pass

    def connect(self, ip: str, port: int):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip, port))
        self.status = 1

    def _blockTillFound(self, callback): # TODO maybe nasty mit dem Callback
        text = ""
        while "found" not in text:
            text = text + self.s.recv(1024).decode("UTF-8")
        self.status = 2
        callback("We found an opponent for you. You can start playing ... just select and transmit useing the 'Ausführen' button")

    def waitTillFound(self, callback):
        if self.status != 2:
            a = threading.Thread(target=self._blockTillFound, args=[callback])
            a.start()

    def earn(self):
        data = self.s.recv(1024).decode("UTF-8").split(';')
        self.message = data[0]
        self.p2Choice = data[1].rsplit("\n")[0]
        print(self.p2Choice)
        if data[0] == "won":
            self.p1Points += 1
        elif data[0] == "lost":
            self.p2Points += 1
        self.rounds += 1

    def play(self, choice: str):
        self.s.sendall((choice + "\n").encode('UTF-8'))

    def getP2Choice(self) -> str:
        return self.p2Choice

    def disconnect(self):
        self.s.sendall('disconnect\n'.encode('UTF-8'))
        self.s.close()
        self.status = 0
