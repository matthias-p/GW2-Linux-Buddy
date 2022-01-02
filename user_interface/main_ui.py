from typing import List
import threading

from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QAction, \
    QAbstractItemView, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt

from game_utils.client_list import ClientList, Client
from game_utils.exceptions.process_not_running_exception import ProcessNotRunningException
from lb_settings.settings import Settings
from user_interface.add_account_ui import AddAccountUI
from user_interface.settings_ui import SettingsUI


class MainUI(QMainWindow):
    def __init__(self, settings: Settings):
        super(MainUI, self).__init__()
        self.settings = settings
        self.client_list = ClientList(settings=settings)

        # References to different UI elements
        self.settings_ui = SettingsUI(settings=settings)
        self.add_account_ui = AddAccountUI(client_list=self.client_list,
                                           callback=self.populate_client_table_widget)

        # UI elements
        self.client_table_widget = QTableWidget()

        self.launch_btn = QPushButton("Launch")

        self._init_ui()

    def _init_ui(self):
        # Menubar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.setStatusTip("Exit Application")
        exit_action.triggered.connect(lambda _: print("exit"))

        file_menu.addAction(exit_action)

        account_menu = menubar.addMenu("Account")
        add_account_action = QAction("Add account", self)
        add_account_action.triggered.connect(self.add_account_action_triggered)

        update_account_action = QAction("Update accounts", self)
        update_account_action.setStatusTip("This patches the locales to the latest versions")
        update_account_action.triggered.connect(self.update_account_action_triggered)

        account_menu.addAction(add_account_action)
        account_menu.addAction(update_account_action)

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.show_settings_ui)

        menubar.addAction(settings_action)

        # Statusbar
        self.statusBar()

        # UI Elements
        self.client_table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.client_table_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.client_table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.client_table_widget.setColumnCount(3)
        self.client_table_widget.setHorizontalHeaderLabels(["Account Name", "Process", "PID"])
        self.client_table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.client_table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.client_table_widget.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.populate_client_table_widget()

        self.launch_btn.clicked.connect(self.launch_btn_clicked)

        # Layout
        central_layout = QVBoxLayout()
        central_layout.addWidget(self.client_table_widget)
        central_layout.addWidget(self.launch_btn)

        central_widget = QWidget()
        central_widget.setLayout(central_layout)

        self.setCentralWidget(central_widget)

        self.resize(640, 480)
        self.setWindowTitle("Linux Buddy")

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        for client_name in self.client_list:
            try:
                self.client_list.get_client(client_name).stop()
            except ProcessNotRunningException:
                pass

    def show_settings_ui(self):
        self.settings_ui.show()

    def populate_client_table_widget(self):
        self.client_table_widget.setRowCount(0)
        for client in self.client_list:
            c = self.client_list.get_client(client)
            rows = self.client_table_widget.rowCount()
            self.client_table_widget.insertRow(rows)

            self.client_table_widget.setItem(rows, 0, QTableWidgetItem(client))
            self.client_table_widget.setItem(rows, 1, QTableWidgetItem(
                "Running" if c.process is not None else "Not Running"))
            self.client_table_widget.setItem(rows, 2, QTableWidgetItem(
                c.process.pid if c.process is not None else "n/a"))

    def add_account_action_triggered(self):
        self.add_account_ui.show()

    def update_account_action_triggered(self):
        self.client_list.patch_all()

    def launch_btn_clicked(self):
        row: List[QTableWidgetItem] = self.client_table_widget.selectedItems()
        client: Client = self.client_list.get_client(row[0].text())
        client.launch()
        row[1].setText("Running")
        row[2].setText(str(client.process.pid))

        threading.Thread(target=client.poll_status, args=(self.reset_client_process, )).start()

    def reset_client_process(self, client: Client):
        x: QTableWidgetItem = self.client_table_widget.findItems(client.name, Qt.MatchContains)[0]
        self.client_table_widget.item(x.row(), 1).setText("Not Running")
        self.client_table_widget.item(x.row(), 2).setText("n/a")
