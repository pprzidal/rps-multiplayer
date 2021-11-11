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

        try:
            self.model.connect()
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
        self.view.setP1Choice(choice)
        self.view.setP2choice(self.model.getP2Choice())
        self.view.setPoints(self.model.p1Points, self.model.p2Points)
        self.view.setRounds(f"{self.model.rounds}")
        self.view.setStatus(f"You have {self.model.message}")


if __name__ == '__main__':
    app = QApplication([])
    c = Controller()
    c.view.show()
    sys.exit(app.exec())
