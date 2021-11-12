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

        try:
            self.model.connect(ip, port)
            self.view.setStatus("Verbunden mit Server")
        except:
            import traceback
            traceback.print_exc()
            self.view.setStatus("Fehler: Konnte sich nicht mit dem Client verbinden")

    def reset(self):
        self.model.reset()
        self.view.reset()

    def play(self):
        choice = self.view.getPlayerChoice()
        self.model.play(choice)
        self.model.earn()
        #einThread = threading.Thread(target=self.model.earn)
        #einThread.start()
        #einThread.join()
        #self.model.earn()
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
    app = QApplication([])
    c = Controller(ip, port)
    c.view.show()
    sys.exit(app.exec())
