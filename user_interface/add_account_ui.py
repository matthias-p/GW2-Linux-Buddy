from typing import Callable

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout

from game_utils.client_list import ClientList


class AddAccountUI(QWidget):
    def __init__(self, client_list: ClientList, callback: Callable):
        """
        Init the Widget
        :param client_list: Client List to add the account to
        :param callback: Callback to update the client_list_view
        """
        super(AddAccountUI, self).__init__()
        self.client_list = client_list
        self.callback = callback

        self.account_name_tbx = QLineEdit()
        self.account_name_lbl = QLabel("Account Name: ")

        self.ok_btn = QPushButton("Ok")
        self.cancel_btn = QPushButton("Cancel")

        self._init_ui()

    def _init_ui(self):
        self.ok_btn.clicked.connect(self.ok_btn_clicked)
        self.cancel_btn.clicked.connect(self.cancel_btn_clicked)

        main_hbox = QHBoxLayout()
        main_hbox.addWidget(self.account_name_lbl)
        main_hbox.addWidget(self.account_name_tbx)

        control_btn_hbox = QHBoxLayout()
        control_btn_hbox.addStretch()
        control_btn_hbox.addWidget(self.ok_btn)
        control_btn_hbox.addWidget(self.cancel_btn)

        central_layout = QVBoxLayout()
        central_layout.addLayout(main_hbox)
        central_layout.addLayout(control_btn_hbox)

        self.setLayout(central_layout)

        self.resize(400, 200)
        self.setWindowTitle("Linux Buddy - Add Account")

    def ok_btn_clicked(self):
        if self.account_name_tbx.text():
            self.client_list.add_client(self.account_name_tbx.text())
            self.callback()
            self.close()

    def cancel_btn_clicked(self):
        self.close()
