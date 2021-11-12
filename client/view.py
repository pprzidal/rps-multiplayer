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
        self.rounds.setText(str(rounds))

    def setPoints(self, p1Points: int, p2Points: int):
        self.p1Points.setText(str(p1Points))
        self.p2Points.setText(str(p2Points))

    def setPChoice(self, pChoice: str, which: int):
        pix = QPixmap()
        pix.load(f"{pChoice}.jpg")
        if which == 1:
            self.p1Choice.setPixmap(pix)
        elif which == 2:
            self.p2Choice.setPixmap(pix)

    def setStatus(self, message: str):
        self.statusBar().showMessage(message)

