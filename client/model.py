import socket

HOST = '172.20.10.7'
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
        self.s = None

    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))
        self.s.sendall(b'Hello World!')

    def play(self, choice: str):
        self.s.sendall(bytes(choice))

    def disconnect(self):
        self.s.sendall(b'disconnect')


