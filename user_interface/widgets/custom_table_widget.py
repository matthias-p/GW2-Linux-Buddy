from PyQt5 import QtGui
from PyQt5.QtWidgets import QTableWidget, QAbstractItemView, QMenu

from game_utils.client import Client
from user_interface.launch_settings_ui import LaunchSettingsUI


class CustomTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super(CustomTableWidget, self).__init__(parent)
        self.launch_settings_ui = None
        self.client_list = parent.__dict__.get("client_list")

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        menu = QMenu()

        launch_action = menu.addAction("Launch")
        terminate_action = menu.addAction("Terminate")
        launch_settings_action = menu.addAction("Launch Parameters")

        action = menu.exec_(self.mapToGlobal(event.pos()))

        if action == launch_action:
            client: Client = self.client_list.get_client(self.item(self.currentRow(), 0).text())
            if client.process is None:
                client.launch()
        elif action == terminate_action:
            client: Client = self.client_list.get_client(self.item(self.currentRow(), 0).text())
            if client.process is not None:
                client.stop()
        elif action == launch_settings_action:
            self.launch_settings_ui = LaunchSettingsUI(self.item(self.currentRow(), 0).text())
            self.launch_settings_ui.show()
