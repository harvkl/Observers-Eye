# ui_main.py - файл с интерфейсом

#Контейнеры: QWidget, QMainWindow, QDialog, QFrame
#Элементы ввода: QPushButton, QLineEdit, QTextEdit, QCheckBox, QRadioButton
#Отображение данных: QLabel, QTableView, QListView, QTreeView
#Диалоги: QFileDialog, QMessageBox, QInputDialog, QColorDialog
#Компоненты навигации: QTabWidget, QStackedWidget, QToolBar

import sys # доступ к аргументам cmd
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QLabel, 
    QMainWindow, 
    QPushButton, 
    QComboBox, 
    QListWidget, 
    QGridLayout, 
    QVBoxLayout, 
    QHBoxLayout, 
    QStackedLayout,
    QTabWidget)
from logic import Logic
from logic import Color


# подкласс QMainWindow для настройки окна
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Observer's Eye")
        self.setFixedSize(1280, 720)

        #grid_layout = QGridLayout() # Создаем сеточную разметку для организации элементов

        '''layout1 = QStackedLayout()
        layout2 = QVBoxLayout()
        layout3 = QHBoxLayout()

        layout3.addWidget(QPushButton("Perfomance"))
        layout3.addWidget(QPushButton("Results"))
        layout3.addWidget(QPushButton("Info"))


        layout2.addLayout(layout3)
        layout2.addLayout(layout1)

        layout1.addWidget(Color("White"))
        layout1.addWidget(Color("Blue"))
        layout1.addWidget(Color("White"))

        layout1.setCurrentIndex(1) #реализация вкладок через это!!!!!!!!!'''

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.setMovable(True)

        tabs.addTab(Color("Red"), "Perfomance")
        tabs.addTab(Color("Blue"), "Results")
        tabs.addTab(Color("White"), "Info")
        tabs.setTabIcon(0, QIcon("anchor.png"))
        tabs.setTabIcon(1, QIcon("report.png"))
        tabs.setTabIcon(2, QIcon("information.png"))



        #central_widget = QWidget() # создали центральный виджет
        #central_widget.setLayout(layout2) # для макета задаем сеточную разметку
        self.setCentralWidget(tabs) # устанавливаем разметку для окна


        #QListWidget().addItems(["Perfomance", "Results", "Info"])
        #grid_layout.addWidget(Color("Blue"), 0, 0)
        #grid_layout.addWidget(Color("Yellow"), 1, 1)