import socket

HOST = '172.20.10.10'
PORT = 42945


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

    def reset(self):
        pass

    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))
        self.s.sendall(b'Hello World!')

    def play(self, choice: str):
        self.s.sendall(bytes(choice))
        data = self.s.recv(1024).decode("UTF-8")
        self.rounds += 1
        data = data.split(";")
        self.message(data[0])
        if data[0] == "won":
            self.p1Points += 1
        elif data[0] == "lost":
            self.p2Points += 1
        self.rounds += 1
        self.p2Choice = data[1]

    def getP2Choice(self) -> str:
        return self.p2Choice

    def disconnect(self):
        self.s.sendall(b'disconnect')
