# main.py - точка входа

import sys # доступ к аргументам cmd

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from ui_main import MainWindow


def main():
    app = QApplication(sys.argv) # класс QApplication содержит цикл событий и нужен лишь в 1-ом экземпляре
    app.setWindowIcon(QIcon("./media/eye.png"))

    # добавляем в трей
    tray = QSystemTrayIcon()
    tray.setIcon(QIcon("./media/eye.png"))
    tray.setToolTip("Observer's Eye | Monitoring")
    tray.show()

    # создаем подменю для трея
    tray_menu = QMenu()
    exit_tray_menu = QAction("Quit Observer's Eye")
    exit_tray_menu.triggered.connect(app.quit)
    tray_menu.addAction(exit_tray_menu)
    tray.setContextMenu(tray_menu)

    # подгрузка стиля
    with open("./styles/styles.qss", "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())

    # создание окна
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()