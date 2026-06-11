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
        self.setFixedSize(850, 700)

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.setMovable(True)

        # создание объекта логики
        self.logic = Logic()

        # это что то типо виджетов для каждого таба содержащих функцию создающую внутренности таба (другие виджеты)
        perfomance_tab_widget = self.create_perfomance_tab()
        results_tab_widget = self.create_results_tab()
        info_tab_widget = self.create_info_tab()

        tabs.addTab(perfomance_tab_widget, "Performance")
        tabs.addTab(results_tab_widget, "Results")
        tabs.addTab(info_tab_widget, "Info")

        tabs.setTabIcon(0, QIcon("./media/anchor.png"))
        tabs.setTabIcon(1, QIcon("./media/report.png"))
        tabs.setTabIcon(2, QIcon("./media/information.png"))

        self.setCentralWidget(tabs) # устанавливаем разметку для окна

        # создаем таймер для апдейта таба с листом процессов
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_perfomace_tab) # коннектим функцию на таймер
        self.timer.start(3000) # апдейт каждые 3 секунды

        self.update_perfomace_tab()

    #-------------------------------------------------------------------------- создание виджетов внутри табов
    def create_perfomance_tab(self):
        widget = QWidget()
        #widget.setStyleSheet("background-color: #E6E6FA; font-family: 'Roboto', Arial, sans-serif; font-size: 25px;")
        layout = QVBoxLayout(widget)

        self.label = QLabel("PERFORMANCE MONITORING")
        self.current_cpu_status_label = QLabel("CPU: ??")
        self.current_ram_status_label = QLabel("RAM: ??")

        self.cpu_bar = QProgressBar()
        self.cpu_bar.setRange(0, 100)
        self.cpu_bar.setTextVisible(False)

        self.ram_bar = QProgressBar()
        self.ram_bar.setRange(0, 100)
        self.ram_bar.setTextVisible(False)

        self.info_list = QListWidget()
        self.table_info_list = QTableWidget()

        self.info_list.setFixedHeight(425)
        self.info_list.setDisabled(True) # ставим лист по дефолту выключенным
        self.info_list.setVisible(False) # ставим лист по дефолту невидимым
        self.info_list_disabled = True # делаем переменную чтобы понимать когда и что, тк нету функции получения состояния

        self.table_info_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed) # запрещаем изменять ширину колонок
        self.table_info_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff) # убираем навсегда горизонтальный скролл для таблички
        self.table_info_list.setFixedHeight(425)
        self.table_info_list.setColumnCount(4)
        self.table_info_list.setRowCount(230)
        labels = ["PID", "Name", "CPU", "RAM"]
        self.table_info_list.setHorizontalHeaderLabels(labels)
        self.table_info_list.setColumnWidth(0, 100)
        self.table_info_list.setColumnWidth(1, 315)
        self.table_info_list.setColumnWidth(2, 200)
        self.table_info_list.setColumnWidth(3, 198)
        self.table_info_list.verticalHeader().setVisible(False) # убираем видимость номера кортежа
        self.table_info_list.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers) # запрещаем че либо делать со строками
        self.table_info_list.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows) # делаем так что если тыкаем куда либо то выбиралась вся строка
        self.table_info_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection) # делаем так чтобы можно было выбрать только один процесс за раз

        self.kill_button = QPushButton("Select and kill the process")
        self.note_label = QLabel("*Note: the percentage of usage that shows for the System Idle Process shows not the CPU usage, but the percent of available resources for other processes.")
        self.switch_list_table_button = QPushButton("Switch process display mode")

        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.current_cpu_status_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.cpu_bar)
        layout.addWidget(self.current_ram_status_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.ram_bar)
        layout.addWidget(self.info_list)
        layout.addWidget(self.table_info_list)
        layout.addWidget(self.kill_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.note_label, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.switch_list_table_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # коннектим функцию убийства процесса из списка на кнопку кил батон
        self.kill_button.clicked.connect(self.kill_process)
        self.switch_list_table_button.clicked.connect(self.switch_list_table)

        layout.addStretch() # эт строка поглощает спейс при изменении размера окна, но тк в 26 строке у нас задан фиксед размер то эта строка юзлес, но оставим ее в случае если уберем 26 строку

        return widget

    def create_results_tab(self):
        widget = QWidget()
        #widget.setStyleSheet("background-color: #E6E6FA; font-family: 'Roboto', Arial, sans-serif; font-size: 25px;")
        layout = QVBoxLayout(widget)

        self.res_label = QLabel("RESULTS")
        self.save_button = QPushButton("Save the results in .txt file?")

        layout.addWidget(self.res_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # подключаем кнопочку сохранения к методу который сохраняет резы
        self.save_button.clicked.connect(self.save_results)

        return widget

    def create_info_tab(self):
        widget = QWidget()
        #widget.setStyleSheet("background-color: #E6E6FA; font-family: 'Roboto', Arial, sans-serif; font-size: 25px; border: none; padding: 15px 0px 0px 0px;")
        layout = QVBoxLayout(widget)

        self.info_label = QLabel("INFO ABOUT THE PROGRAMM")
        self.text_block = QTextEdit()

        self.text_block.setFixedSize(830, 80)

        self.cpu_stats_since_load = QLabel("")
        self.cpu_usage_avg = QLabel("")
        self.cpu_freq = QLabel("")
        self.boot_time_label = QLabel("")

        self.get_info_tab_button = QPushButton("Get stats!")

        self.users = self.logic.get_users()

        self.text_block.setText(f"Hello, {self.users[0].name}. This is a simple tool that shows us information about the current processes and CPU status. This program was created by an enthusiast, so don't be hard on me.")
        self.text_block.setReadOnly(True)

        layout.addWidget(self.info_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.text_block, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.cpu_stats_since_load)
        layout.addWidget(self.cpu_usage_avg)
        layout.addWidget(self.cpu_freq)
        layout.addWidget(self.boot_time_label)
        layout.addWidget(self.get_info_tab_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # подключаем кнопочку получения инфы к методу получения инфы
        self.get_info_tab_button.clicked.connect(self.get_stats_for_info_tab)

        layout.addStretch() # эт строка поглощает спейс при изменении размера окна, но тк в 26 строке у нас задан фиксед размер то эта строка юзлес, но оставим ее в случае если уберем 26 строку

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

                    f.write("========================================================================================================\n")

                    for process in processes:
                        f.write(f"PID: {process['pid']} | Name: {process['name']} | CPU: {process.get('cpu_percent', 0) / 10:.1f}% | RAM: {process.get('memory_percent', 0):.1f}%\n")

                    f.write("========================================================================================================\n\n")

                    if self.cpu_stats_since_load.text() != "":
                        f.write("\n========================================================================================================")
                        f.write(f"\nCPU stats:\n    Context switches: {self.ctx_switches}\n    Interrupts: {self.interrupts}\n    Soft interrupts: {self.soft_interrupts}\n    System calls: {self.sys_calls}")
                        f.write(f"\n\nSystem AVG load for 1, 5, 15 minutes: {self.l1:.2f}, {self.l5:.2f}, {self.l15:.2f}\n  Current utilization: {self.curr_util:.1f}%")
                        f.write(f"\n\nCurrent CPU frequency: {self.curr_cpu_freq} MHz\n    Minimum CPU frequency: {self.min_cpu_freq} MHz\n    Maximum CPU frequency: {self.max_cpu_freq} MHz")
                        f.write(f"\n\nSystem is running since: {self.readable_time}")
                        f.write("\n========================================================================================================")
                    
                    QMessageBox.information(self, "Success", f"The results were saved in {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Couldn't save: {e}")


    def kill_process(self, pid):
        selected_item = self.info_list.selectedItems() # получаем выбранный итем из списка который удалим

        if self.info_list_disabled: # если у нас таблица
            # пытаемся извлечь пид процесса
            try:
                selected_table_item = self.table_info_list.selectedItems() # получаем выбранный из таблицы итем который удалим
                table_item_text = selected_table_item[0].text()
                pid = int(table_item_text) # извлекаем pid для таблицы
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Pick the process: {e}")
        elif not self.info_list_disabled: # если у нас лист
            # пытаемся извлечь пид процесса
            try:
                selected_item = self.info_list.selectedItems() # получаем выбранный итем из списка который удалим
                item_text = selected_item[0].text()
                pid = int(item_text.split(' | ')[0].split(': ')[1]) # извлекаем pid для списка
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Pick the process: {e}")

        # пытаемся термнуть процесс по его pid'у
        try:
            process_to_kill = psutil.Process(pid)
            process_to_kill.terminate()
            QMessageBox.information(self, "Success", f"Process with PID: {pid} was terminated")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Couldn't kill the process: {e}")

    
    def get_stats_for_info_tab(self):
        
        self.boot_time_timestamp = psutil.boot_time() # получаем время загрузки в виде timestamp
        self.boot_time_datetime = datetime.fromtimestamp(self.boot_time_timestamp) # преобразуем timestamp в объект datetime (используется локальное время)
        self.readable_time = self.boot_time_datetime.strftime("%Y-%m-%d %H:%M:%S") # форматируем в читаемую строку

        self.l1, self.l5, self.l15 = psutil.getloadavg()
        self.cpu_count = psutil.cpu_count(logical=True)
        self.curr_util = ((self.l1 / self.cpu_count) * 100)

        self.ctx_switches = psutil.cpu_stats().ctx_switches
        self.interrupts = psutil.cpu_stats().interrupts
        self.soft_interrupts = psutil.cpu_stats().soft_interrupts
        self.sys_calls = psutil.cpu_stats().syscalls

        self.curr_cpu_freq = round(psutil.cpu_freq().current, 2)
        self.min_cpu_freq = round(psutil.cpu_freq().min, 2)
        self.max_cpu_freq = round(psutil.cpu_freq().max, 2)

        self.cpu_stats_since_load.setText(f"CPU stats:\n    Context switches: {self.ctx_switches}\n    Interrupts: {self.interrupts}\n    Soft interrupts: {self.soft_interrupts}\n    System calls: {self.sys_calls}")
        self.cpu_usage_avg.setText(f"System AVG load for 1, 5, 15 minutes: {self.l1:.2f}, {self.l5:.2f}, {self.l15:.2f}\n  Current utilization: {self.curr_util:.1f}%")
        self.cpu_freq.setText(f"Current CPU frequency: {self.curr_cpu_freq} MHz\n    Minimum CPU frequency: {self.min_cpu_freq} MHz\n    Maximum CPU frequency: {self.max_cpu_freq} MHz")
        self.boot_time_label.setText(f"System is running since: {self.readable_time}")


    def switch_list_table(self):
        if self.info_list_disabled: # если лист выключен то включаем
            self.table_info_list.setDisabled(True)
            self.table_info_list.setVisible(False)
            self.info_list.setDisabled(False)
            self.info_list.setVisible(True)
            self.info_list_disabled = False
        elif not self.info_list_disabled: # если лист включен то выключаем
            self.table_info_list.setDisabled(False)
            self.table_info_list.setVisible(True)
            self.info_list.setDisabled(True)
            self.info_list.setVisible(False)
            self.info_list_disabled = True
