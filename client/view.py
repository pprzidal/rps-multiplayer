from PyQt6.QtGui import QPixmap
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
        self.comboBox.addItem("scissors")
        self.comboBox.addItem("rock")
        self.comboBox.addItem("paper")
        self.pb_exec.clicked.connect(c.play)
        self.pb_reset.clicked.connect(c.reset)

    def reset(self):
        pass

    def getPlayerChoice(self):
        return self.comboBox.currentText()

    def setRounds(self, rounds: int):
        self.rounds.setText(rounds)

    def setPoints(self, p1Points: int, p2Points: int):
        self.p1Points.setText(p1Points)
        self.p2Points.setText(p2Points)

    def setP1Choice(self, p1Choice: str):
        pix = QPixmap()
        if p1Choice == "scissors":
            pix.load("schere.jpg")
        elif p1Choice == "rock":
            pix.load("stein.jpg")
        elif p1Choice == "paper":
            pix.load("papier.jpg")
        self.p1Choice.setPixmap(pix)

    def setP2choice(self, p2Choice: str):
        pix = QPixmap()
        if p2Choice == "scissors":
            pix.load("schere.jpg")
        elif p2Choice == "rock":
            pix.load("stein.jpg")
        elif p2Choice == "paper":
            pix.load("papier.jpg")
        self.p2Choice.setPixmap(pix)

    def setStatus(self, message: str):
        self.statusBar().showMessage(message)

