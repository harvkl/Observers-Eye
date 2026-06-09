# logic.py - файл с логикой

import sys # доступ к аргументам cmd
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QPushButton, QComboBox, QListWidget, QGridLayout
from PyQt6.QtGui import QPalette, QColor
import psutil

class Logic:
    # класс где будет хранится вся логика приложения

    @staticmethod
    def get_process_list():
        processes = []

        for process in psutil.process_iter([
            'pid',
            'name',
            'cpu_percent',
            'memory_percent'
        ]):
            try:
                processes.append(process.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True) #сортировка по убыванию

        #return processes[:40] # возвращаем 40 процессов
        return processes
    
    @staticmethod
    def get_users():
        users = []

        users = psutil.users()

        return users
    
    
class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)