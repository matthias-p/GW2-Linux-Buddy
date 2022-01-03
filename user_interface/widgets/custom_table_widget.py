from PyQt5 import QtGui
from PyQt5.QtWidgets import QTableWidget, QAbstractItemView, QMenu

from game_utils.client import Client
from game_utils.client_list import ClientList
from user_interface.launch_settings_ui import LaunchSettingsUI


class CustomTableWidget(QTableWidget):
    def __init__(self, parent=None, client_list: ClientList = None):
        super(CustomTableWidget, self).__init__(parent)
        self.launch_settings_ui = None
        self.client_list = client_list

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        menu = QMenu()

        terminate_action = menu.addAction("Terminate")
        launch_settings_action = menu.addAction("Launch Parameters")

        action = menu.exec_(self.mapToGlobal(event.pos()))

        if action == terminate_action:
            client: Client = self.client_list.get_client(self.item(self.currentRow(), 0).text())
            if client.process is not None:
                client.stop()
        elif action == launch_settings_action:
            self.launch_settings_ui = LaunchSettingsUI(self.client_list.get_client(
                self.item(self.currentRow(), 0).text()))
            self.launch_settings_ui.show()
