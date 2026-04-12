# ui_main.py - файл с интерфейсом

#Контейнеры: QWidget, QMainWindow, QDialog, QFrame
#Элементы ввода: QPushButton, QLineEdit, QTextEdit, QCheckBox, QRadioButton
#Отображение данных: QLabel, QTableView, QListView, QTreeView
#Диалоги: QFileDialog, QMessageBox, QInputDialog, QColorDialog
#Компоненты навигации: QTabWidget, QStackedWidget, QToolBar

import sys # доступ к аргументам cmd
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QPushButton, QComboBox, QListWidget, QGridLayout
from logic import Logic
from logic import Color


# подкласс QMainWindow для настройки окна
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Observer's Eye")
        self.setFixedSize(1280, 720)


        central_widget = QWidget() # создали центральный виджет / макет
        grid_layout = QGridLayout() # Создаем сеточную разметку для организации элементов

        central_widget.setLayout(grid_layout) # для макета задаем сеточную разметку
        self.setCentralWidget(central_widget) # устанавливаем разметку для окна


        #widget = QListWidget()
        #widget.addItems(["Perfomance", "Results", "Info"])
        grid_layout.addWidget(Color("Red"), 0, 0)
        grid_layout.addWidget(Color("Green"), 0, 0)
        grid_layout.addWidget(Color("Blue"), 0, 0)


if __name__ == "__main__":
    app = QApplication(sys.argv) # класс QApplication содержит цикл событий и нужен лишь в 1-ом экземпляре
    # создание окна
    window = MainWindow()
    window.show()
    sys.exit(app.exec())