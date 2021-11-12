import view
import model
import sys
import threading
from PyQt6.QtWidgets import QApplication


class Controller:
    """
    Klasse die sich um die Kommunikation zwischen dem Model und der View kümmert
    """

    def __init__(self, ip, port):
        self.view = view.View(self)
        self.model = model.Model()
        self.ip = ip
        self.port = port


    def reset(self):
        self.model.reset()
        self.view.reset()

    def connect(self):
        try:
            self.model.connect(self.ip, self.port)
            self.view.setStatus("Connected to Server. Waiting for Opponent")
            self.model.waitTillFound(self.setStatus)
        except:
            import traceback
            traceback.print_exc()
            #print('yo')
            self.view.setStatus("Error: Couldn't connect to Server")

    def play(self):
        if self.model.status != 2:
            return
        choice = self.view.getPlayerChoice()
        self.model.play(choice)
        self.model.earn()
        self.view.setPChoice(choice, 1)
        self.view.setPChoice(self.model.getP2Choice(), 2)
        self.view.setPoints(self.model.p1Points, self.model.p2Points)
        self.view.setRounds(self.model.rounds)
        # TODO kinda nasty
        self.view.setStatus(f"You have {'tied' if self.model.message == 'tie' else self.model.message}")

    def setStatus(self, msg):
        self.view.setStatus(msg)


if __name__ == '__main__':
    try:
        ip = sys.argv[1]
        port = int(sys.argv[2])
    except Exception: # weil value error mit dem parsen vom port und dem Fall das der user nur "python main.py" macht
        print('Usage works like this: python controller.py <ip> <port>\nport has to be a parsable int')
        sys.exit(1)
    app = QApplication([])
    c = Controller(ip, port)
    c.view.show()
    c.connect()
    sys.exit(app.exec())
