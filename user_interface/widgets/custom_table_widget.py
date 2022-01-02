from PyQt5 import QtGui
from PyQt5.QtWidgets import QTableWidget, QAbstractItemView, QMenu, qApp

from game_utils.client import Client


class CustomTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super(CustomTableWidget, self).__init__(parent)
        self.client_list = parent.__dict__.get("client_list")

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        menu = QMenu()

        terminate_action = menu.addAction("Terminate")

        action = menu.exec_(self.mapToGlobal(event.pos()))

        if action == terminate_action:
            client: Client = self.client_list.get_client(self.item(self.currentRow(), 0).text())
            if client.process is not None:
                client.stop()
