from PyQt6.QtWidgets import *
from PyQt6 import uic

from controller import Controller


class View(QMainWindow):
    """
    Zeigt die GUI an und kümmert sich um Änderungen
    """

    def __init__(self, c: Controller):
        super().__init__()
        uic.loadUi("mainwindow.ui", self)
        self.comboBox.addItem("Schere")
        self.comboBox.addItem("Stein")
        self.comboBox.addItem("Papier")
        self.pb_exec.clicked.connect(c.play)
        self.pb_reset.clicked.connect(c.reset)

    def getPlayerChoice(self):
        return self.comboBox.currentText()

    def setRounds(self, rounds: int):
        self.rounds.setText(rounds)

    def setPoints(self, p1Points: int, p2Points: int):
        self.p1Points.setText(p1Points)
        self.p2Points.setText(p2Points)

    def setP1Choice(self, p1Choice: str):
        pass

    def setP2choice(self, p2Choice: str):
        pass

    def setStatus(self, message: str):
        self.statusBar().showMessage(message)