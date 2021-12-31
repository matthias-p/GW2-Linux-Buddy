import sys

from PyQt5.QtWidgets import QApplication

from lb_settings.settings import Settings
from user_interface.main_ui import MainUI


def main():
    settings = Settings()
    app = QApplication(sys.argv)
    main_ui = MainUI(settings)
    main_ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
