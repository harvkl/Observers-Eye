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

from logic import Logic
from logic import Color
from datetime import datetime
import psutil


# подкласс QMainWindow для настройки окна
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Observer's Eye")
        self.setFixedSize(850, 600)

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

        tabs.setTabIcon(0, QIcon("./media/anchor.png"))
        tabs.setTabIcon(1, QIcon("./media/report.png"))
        tabs.setTabIcon(2, QIcon("./media/information.png"))

        self.setCentralWidget(tabs) # устанавливаем разметку для окна

        # создаем таймер для апдейта таба с листом процессов
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_perfomace_tab) # коннектим функцию на таймер
        self.timer.start(4000) # апдейт каждые 4 секунды

        self.update_perfomace_tab()

    #-------------------------------------------------------------------------- создание виджетов внутри табов
    def create_perfomance_tab(self):
        widget = QWidget()
        #widget.setStyleSheet("background-color: #E6E6FA; font-family: 'Roboto', Arial, sans-serif; font-size: 25px;")
        layout = QVBoxLayout(widget)

        self.label = QLabel("PERFOMANCE MONITORING")
        self.current_cpu_status_label = QLabel("CPU: ??")
        self.current_ram_status_label = QLabel("RAM: ??")

        self.cpu_bar = QProgressBar()
        self.cpu_bar.setRange(0, 100)
        self.cpu_bar.setTextVisible(True)

        self.ram_bar = QProgressBar()
        self.ram_bar.setRange(0, 100)
        self.ram_bar.setTextVisible(True)

        self.info_list = QListWidget()
        self.table_info_list = QTableWidget()

        self.table_info_list.setColumnCount(4)
        self.table_info_list.setRowCount(230)
        labels = ["PID", "Name", "CPU", "RAM"]
        self.table_info_list.setHorizontalHeaderLabels(labels)

        self.kill_button = QPushButton("Select and kill process")
        self.note_label = QLabel("*Note: a percentage of usage, that shows for System Idle Process, shows not the CPU usage, but the percent of available resources for other processes.")

        layout.addWidget(self.label)
        layout.addWidget(self.current_cpu_status_label)
        layout.addWidget(self.cpu_bar)
        layout.addWidget(self.current_ram_status_label)
        layout.addWidget(self.ram_bar)
        layout.addWidget(self.info_list)
        layout.addWidget(self.table_info_list)
        layout.addWidget(self.kill_button)
        layout.addWidget(self.note_label)
        #info_list.addItems(["1st", "2nd", "3rd"])
        
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #self.info_list.setAlignment(Qt.AlignmentFlag.AlignCenter)


        # коннектим функцию убийства процесса из списка на кнопку кил батон
        self.kill_button.clicked.connect(self.kill_process)

        layout.addStretch() # эт строка поглощает спейс при изменении размера окна, но тк в 26 строке у нас задан фиксед размер то эта строка юзлес, но оставим ее в случае если уберем 26 строку

        return widget

    def create_results_tab(self):
        widget = QWidget()
        #widget.setStyleSheet("background-color: #E6E6FA; font-family: 'Roboto', Arial, sans-serif; font-size: 25px;")
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
        #widget.setStyleSheet("background-color: #E6E6FA; font-family: 'Roboto', Arial, sans-serif; font-size: 25px; border: none; padding: 15px 0px 0px 0px;")
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
        self.current_cpu_status_label.clear()
        self.current_ram_status_label.clear()

        curr_cpu_usage = psutil.cpu_percent()
        curr_ram_usage = psutil.virtual_memory().percent

        # добавили всплывающие предупреждалки при высокой загруженности CPU и RAM
        if curr_cpu_usage > 90:
            QMessageBox.warning(self, "Warning", f"CPU usage is above normal: {curr_cpu_usage}, take actions!")
        if curr_ram_usage > 80:
            QMessageBox.warning(self, "Warning", f"RAM usage is above normal: {curr_ram_usage}, take actions!")

        self.current_cpu_status_label.setText(f"CPU: {curr_cpu_usage}%")
        self.current_ram_status_label.setText(f"RAM: {curr_ram_usage}%")
        self.cpu_bar.setValue(int(curr_cpu_usage))
        self.ram_bar.setValue(int(curr_ram_usage))

        processes = self.logic.get_process_list()

        i = int(0) # делаем итератор для строки в таблице
        for process in processes:

            # получаем все че нам нужно из процесса
            table_pid = f"{process['pid']}"
            table_name = f"{process['name']}"
            table_cpu = f"{process.get('cpu_percent', 0) / 10:.1f}"
            table_ram = f"{process.get('memory_percent', 0):.1f}"

            # делаем строчку которую будем пихать в лист
            string_to_list = f"PID: {table_pid} | Name: {table_name} | CPU: {table_cpu}% | RAM: {table_ram}%"

            self.info_list.addItem(string_to_list)

            self.table_info_list.setItem(i, 0, QTableWidgetItem(table_pid))
            self.table_info_list.setItem(i, 1, QTableWidgetItem(table_name))
            self.table_info_list.setItem(i, 2, QTableWidgetItem(f"{table_cpu}%"))
            self.table_info_list.setItem(i, 3, QTableWidgetItem(f"{table_ram}%"))

            i += 1
    


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
                    f.write(f"CPU: {psutil.cpu_percent()}% | RAM: {psutil.virtual_memory().percent}% on {now}\n\n")
                    f.write(f"Processes in descending order by CPU on {now}\n\n")

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
