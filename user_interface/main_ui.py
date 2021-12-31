from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QAction, QListWidget, \
    QAbstractItemView

from game_utils.client_list import ClientList
from lb_settings.settings import Settings
from user_interface.settings_ui import SettingsUI
from user_interface.add_account_ui import AddAccountUI


class MainUI(QMainWindow):
    def __init__(self, settings: Settings):
        super(MainUI, self).__init__()
        self.settings = settings
        self.client_list = ClientList(settings=settings)

        # References to different UI elements
        self.settings_ui = SettingsUI(settings=settings)
        self.add_account_ui = AddAccountUI(client_list=self.client_list,
                                           callback=self.populate_client_list_view)

        # UI elements
        self.client_list_view = QListWidget()

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
        self.client_list_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.populate_client_list_view()

        self.launch_btn.clicked.connect(self.launch_btn_clicked)

        # Layout
        central_layout = QVBoxLayout()
        central_layout.addWidget(self.client_list_view)
        central_layout.addWidget(self.launch_btn)

        central_widget = QWidget()
        central_widget.setLayout(central_layout)

        self.setCentralWidget(central_widget)

        self.resize(640, 480)
        self.setWindowTitle("Linux Buddy")

    def show_settings_ui(self):
        self.settings_ui.show()

    def populate_client_list_view(self):
        self.client_list_view.clear()
        self.client_list_view.addItems(self.client_list)

    def add_account_action_triggered(self):
        self.add_account_ui.show()

    def update_account_action_triggered(self):
        self.client_list.patch_all()

    def launch_btn_clicked(self):
        pass
