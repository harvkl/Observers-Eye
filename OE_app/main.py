# main.py - точка входа

import sys # доступ к аргументам cmd
from PyQt6.QtWidgets import QApplication
from ui_main import MainWindow


def main():
    app = QApplication(sys.argv) # класс QApplication содержит цикл событий и нужен лишь в 1-ом экземпляре
    # создание окна
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()