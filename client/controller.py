import view
import model
import sys
import threading
from PyQt6.QtWidgets import QApplication


class Controller:
    """
    Klasse die sich um die Kommunikation zwischen dem Model und der View kümmert
    """

    def __init__(self):
        self.view = view.View(self)
        self.model = model.Model()


    def reset(self):
        self.model.reset()
        self.view.reset()

    def connect(self, ip: str, port: int):
        try:
            self.model.connect(ip, port)
            self.view.setStatus("Connected to Server. Waiting for Opponent")
        except:
            import traceback
            traceback.print_exc()
            self.view.setStatus("Error: Couldn't connect to Server")

    def play(self):
        if self.model.waitTillFound() != 1:
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


if __name__ == '__main__':
    try:
        ip = sys.argv[1]
        port = int(sys.argv[2])
    except Exception:
        print('Usage works like this: python controller.py <ip> <port>\nport has to be a parsable int')
        sys.exit(1)
    app = QApplication([])
    c = Controller()
    c.view.show()
    c.connect(ip, port)
    sys.exit(app.exec())
