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

    def setRounds(self, rounds: int):
        pass

    def setPoints(self, p1Points: int, p2Points: int):
        self.p1Points.setText(p1Points)
        self.p2Points.setText(p2Points)

    def setChoices(self, p1Choice: str, p2Choice):
        pass

    def setStatus(self, message: str):
        self.statusBar().showMessage(message)