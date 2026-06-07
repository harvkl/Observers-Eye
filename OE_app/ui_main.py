# ui_main.py - файл с интерфейсом

#Контейнеры: QWidget, QMainWindow, QDialog, QFrame
#Элементы ввода: QPushButton, QLineEdit, QTextEdit, QCheckBox, QRadioButton
#Отображение данных: QLabel, QTableView, QListView, QTreeView
#Диалоги: QFileDialog, QMessageBox, QInputDialog, QColorDialog
#Компоненты навигации: QTabWidget, QStackedWidget, QToolBar

import sys # доступ к аргументам cmd
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
'''from PyQt6.QtCore import QSize, Qt
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
    QTabWidget)'''
from logic import Logic
from logic import Color
from datetime import datetime
import psutil


# подкласс QMainWindow для настройки окна
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Observer's Eye")
        self.setFixedSize(800, 600)

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.setMovable(True)

        # создание объекта логики
        self.logic = Logic()

        # это что то типо виджетов для каждого таба содержащих функцию создающую внутренности таба (другие виджеты)
        perfomance_tab_widget = self.create_perfomance_tab()
        results_tab_widget = self.create_results_tab()
        info_tab_widget = self.create_info_tab()

        tabs.addTab(perfomance_tab_widget, "Perfomance")
        tabs.addTab(results_tab_widget, "Results")
        tabs.addTab(info_tab_widget, "Info")

        tabs.setTabIcon(0, QIcon("anchor.png"))
        tabs.setTabIcon(1, QIcon("report.png"))
        tabs.setTabIcon(2, QIcon("information.png"))

        self.setCentralWidget(tabs) # устанавливаем разметку для окна

        # создаем таймер для апдейта таба с листом процессов
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_perfomace_tab) # коннектим функцию на таймер
        self.timer.start(5000) # апдейт каждые 5 секунд

        self.update_perfomace_tab()

    #-------------------------------------------------------------------------- создание виджетов внутри табов
    def create_perfomance_tab(self):
        widget = QWidget()
        widget.setStyleSheet("background-color: #E6E6FA; font-family: 'Roboto', Arial, sans-serif; font-size: 25px;")
        layout = QVBoxLayout(widget)

        self.label = QLabel("PERFOMANCE MONITORING")
        self.info_list = QListWidget()
        self.kill_button = QPushButton("Select and kill processes")

        layout.addWidget(self.label)
        layout.addWidget(self.info_list)
        layout.addWidget(self.kill_button)
        #info_list.addItems(["1st", "2nd", "3rd"])
        
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #self.info_list.setAlignment(Qt.AlignmentFlag.AlignCenter)


        # коннектим функцию убийства процесса из списка на кнопку кил батон
        self.kill_button.clicked.connect(self.kill_process)


        layout.addStretch()

        return widget

    def create_results_tab(self):
        widget = QWidget()
        widget.setStyleSheet("background-color: #E6E6FA; font-family: 'Roboto', Arial, sans-serif; font-size: 25px;")
        layout = QVBoxLayout(widget)

        self.res_label = QLabel("RESULTS")
        self.save_button = QPushButton("Save results in .txt file?")

        layout.addWidget(self.res_label)
        layout.addWidget(self.save_button)

        self.res_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #self.save_button.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # подключаем кнопочку сохранения к методу который сохраняет резы
        self.save_button.clicked.connect(self.save_results)

        return widget

    def create_info_tab(self):
        widget = QWidget()
        widget.setStyleSheet("background-color: #E6E6FA; font-family: 'Roboto', Arial, sans-serif; font-size: 25px; border: none; padding: 15px 0px 0px 0px;")
        layout = QVBoxLayout(widget)

        self.info_label = QLabel("INFO ABOUT PROGRAMM")
        self.text_block = QTextEdit()

        self.users = self.logic.get_users()

        self.text_block.setText(f"Hello, {self.users[0].name}. It's a simple tool that shows us the information about current processes and cpu status. This programm made by a begginer, so don't be hard on me.")
        self.text_block.setReadOnly(True)

        layout.addWidget(self.info_label)
        layout.addWidget(self.text_block)

        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_block.setAlignment(Qt.AlignmentFlag.AlignBottom)

        layout.addStretch()

        return widget
    #--------------------------------------------------------------------------

    def update_perfomace_tab(self):

        self.info_list.clear()
        processes = self.logic.get_process_list()

        for process in processes:
            # делаем строчку которую будем пихать в лист
            string_to_list = f"PID: {process['pid']} | Name: {process['name']} | CPU: {process.get('cpu_percent', 0) / 10:.1f}% | RAM: {process.get('memory_percent', 0):.1f}%"

            self.info_list.addItem(string_to_list)
    


    def save_results(self):
        # получаем процессы и текущую дату время
        processes = self.logic.get_process_list()
        now = datetime.now().strftime("%Y-%m-%d Time: %H:%M:%S")

        # Диалог сохранения файла
        file_path, _ = QFileDialog.getSaveFileName(self, "Save results", "./Results/", "Text Files (*.txt);;All Files (*)")

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"Report to {self.users[0].name} | Observer's Eye |\n")
                    f.write("——————————————————————————————————\n\n")
                    f.write(f"Top 20 CPU processes on {now}:\n\n")

                    f.write("============================================================\n")

                    for process in processes:
                        f.write(f"PID: {process['pid']} | Name: {process['name']} | CPU: {process.get('cpu_percent', 0) / 10:.1f}% | RAM: {process.get('memory_percent', 0):.1f}%\n")

                    f.write("============================================================")
                    
                    QMessageBox.information(self, "Success", f"Results were saved in {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Couldn't save: {e}")

    def kill_process(self, pid):
        selected_item = self.info_list.selectedItems() # получаем выбранный итем который удалим

        # пытаемся извлечь пид процесса
        try:
            item_text = selected_item[0].text()
            pid = int(item_text.split(' | ')[0].split(': ')[1]) # извлекаем pid
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Pick the process: {e}")

        # пытаемся термнуть процесс по его pid'у
        try:
            process_to_kill = psutil.Process(pid)
            process_to_kill.terminate()
            QMessageBox.information(self, "Success", f"Process with PID: {pid} was terminated")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Couldn't kill the process: {e}")

