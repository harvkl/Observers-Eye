# файл с графикой

#Контейнеры: QWidget, QMainWindow, QDialog, QFrame
#Элементы ввода: QPushButton, QLineEdit, QTextEdit, QCheckBox, QRadioButton
#Отображение данных: QLabel, QTableView, QListView, QTreeView
#Диалоги: QFileDialog, QMessageBox, QInputDialog, QColorDialog
#Компоненты навигации: QTabWidget, QStackedWidget, QToolBar

import sys # доступ к аргументам cmd
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QPushButton, QComboBox, QListWidget, QGridLayout
from logic import Logic


# подкласс QMainWindow для настройки окна
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Observer's Eye")
        self.setFixedSize(1280, 720)

        # создали центральный виджет
        central_widget = QWidget() 

        # Создаем сеточную разметку для организации элементов
        grid_layout = QGridLayout()

        central_widget.setLayout(grid_layout)

        # Устанавливаем разметку для окна
        self.setCentralWidget(central_widget)

        widget = QListWidget()
        widget.addItems(["Perfomance", "Results", "Info"])
        grid_layout.addWidget(widget, 0, 0)


if __name__ == "__main__":
    app = QApplication(sys.argv) # класс QApplication содержит цикл событий и нужен лишь в 1-ом экземпляре
    # создание окна
    window = MainWindow()
    window.show()
    sys.exit(app.exec())