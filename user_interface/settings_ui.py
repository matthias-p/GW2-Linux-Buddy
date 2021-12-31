from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, \
    QFileDialog

from lb_settings.settings import Settings


class SettingsUI(QWidget):
    def __init__(self, settings: Settings):
        super(SettingsUI, self).__init__()
        self.settings = settings

        self.wineprefix_path_lbl = QLabel("Wineprefix Path")
        self.wineprefix_path_tbx = QLineEdit(str(self.settings.wineprefix_path))
        self.wineprefix_path_btn = QPushButton("...")

        self.gamelauncher_path_lbl = QLabel("Gamelauncher Path")
        self.gamelauncher_path_tbx = QLineEdit(str(self.settings.gamelauncher_path))
        self.gamelauncher_path_btn = QPushButton("...")

        self.ok_btn = QPushButton("Ok")
        self.cancel_btn = QPushButton("Cancel")

        self._init_ui()

    def _init_ui(self):
        self.wineprefix_path_tbx.setReadOnly(True)
        self.gamelauncher_path_tbx.setReadOnly(True)

        self.wineprefix_path_btn.clicked.connect(self.wineprefix_btn_clicked)
        self.gamelauncher_path_btn.clicked.connect(self.gamelauncher_btn_clicked)

        self.ok_btn.clicked.connect(self.ok_btn_clicked)
        self.cancel_btn.clicked.connect(self.cancel_btn_clicked)

        label_vbox = QVBoxLayout()
        label_vbox.addWidget(self.wineprefix_path_lbl)
        label_vbox.addWidget(self.gamelauncher_path_lbl)

        textbox_vbox = QVBoxLayout()
        textbox_vbox.addWidget(self.wineprefix_path_tbx)
        textbox_vbox.addWidget(self.gamelauncher_path_tbx)

        btn_vbox = QVBoxLayout()
        btn_vbox.addWidget(self.wineprefix_path_btn)
        btn_vbox.addWidget(self.gamelauncher_path_btn)

        main_hbox = QHBoxLayout()
        main_hbox.addLayout(label_vbox)
        main_hbox.addLayout(textbox_vbox)
        main_hbox.addLayout(btn_vbox)

        control_btn_hbox = QHBoxLayout()
        control_btn_hbox.addStretch()
        control_btn_hbox.addWidget(self.ok_btn)
        control_btn_hbox.addWidget(self.cancel_btn)

        central_layout = QVBoxLayout()
        central_layout.addLayout(main_hbox)
        central_layout.addLayout(control_btn_hbox)

        self.setLayout(central_layout)

        self.resize(500, 200)
        self.setWindowTitle("Linux Buddy - Settings")

    def wineprefix_btn_clicked(self):
        dirname = QFileDialog.getExistingDirectory(self, "Select Wineprefix dir")
        if dirname:
            self.settings.set_wineprefix_path(dirname)
            self.wineprefix_path_tbx.setText(dirname)

    def gamelauncher_btn_clicked(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Gamelauncher")
        if filename:
            self.settings.set_gamelauncher_path(filename)
            self.gamelauncher_path_tbx.setText(filename)

    def ok_btn_clicked(self):
        self.settings.save()
        self.close()

    def cancel_btn_clicked(self):
        self.close()
