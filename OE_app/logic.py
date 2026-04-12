# logic.py - файл с логикой

import sys # доступ к аргументам cmd
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QPushButton, QComboBox, QListWidget, QGridLayout
from PyQt6.QtGui import QPalette, QColor

class Logic:
    # класс где будет хранится вся логика приложения

    def blabla():
        return "blabla"
    
class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)