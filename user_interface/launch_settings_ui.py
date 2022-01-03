"""Settings for launch cl paramenters"""
from pathlib import Path

from PyQt5.QtWidgets import QWidget, QCheckBox, QVBoxLayout, QLabel, QHBoxLayout, QPushButton

from game_utils.launch_settings import LaunchSettings


class LaunchSettingsUI(QWidget):
    def __init__(self, account_name: str):
        super(LaunchSettingsUI, self).__init__()
        self.account_name = account_name
        self.launch_settings = LaunchSettings(account_name)

        self.autologin_cbx = QCheckBox()
        self.bmp_cbx = QCheckBox()
        self.dx11_cbx = QCheckBox()
        self.dx9_cbx = QCheckBox()
        self.forwardrenderer_cbx = QCheckBox()
        self.image_cbx = QCheckBox()
        self.log_cbx = QCheckBox()
        self.mapLoadInfo_cbx = QCheckBox()
        self.nodelta_cbx = QCheckBox()
        self.nomusic_cbx = QCheckBox()
        self.nosound_cbx = QCheckBox()
        self.noui_cbx = QCheckBox()
        self.prefreset_cbx = QCheckBox()
        self.repair_cbx = QCheckBox()
        self.uispanallmonitors_cbx = QCheckBox()
        self.useOldFov_cbx = QCheckBox()
        self.verify_cbx = QCheckBox()
        self.windowed_cbx = QCheckBox()

        self.ok_btn = QPushButton("Ok")
        self.cancel_btn = QPushButton("Cancel")

        self.cbx_list = [self.autologin_cbx, self.bmp_cbx, self.dx11_cbx,
                         self.dx9_cbx, self.forwardrenderer_cbx, self.image_cbx,
                         self.log_cbx, self.mapLoadInfo_cbx, self.nodelta_cbx,
                         self.nomusic_cbx, self.nosound_cbx, self.noui_cbx,
                         self.prefreset_cbx, self.repair_cbx, self.uispanallmonitors_cbx,
                         self.useOldFov_cbx, self.verify_cbx, self.windowed_cbx,
                         ]

        self.mapping = {}
        for cbx, value in zip(self.cbx_list, self.launch_settings.__dict__):
            self.mapping[cbx] = value

        self.init_ui()

    def init_ui(self):
        for cbx in self.cbx_list:
            cbx.stateChanged.connect(self.cbx_state_changed)

        self.ok_btn.clicked.connect(self.ok_btn_pressed)
        self.cancel_btn.clicked.connect(self.cancel_btn_pressed)

        base_vbox = QVBoxLayout()
        for (name, value), cbx in zip(self.launch_settings.__dict__.items(), self.cbx_list):
            cbx.setChecked(value)
            hbox = QHBoxLayout()
            hbox.addWidget(QLabel(name))
            hbox.addStretch()
            hbox.addWidget(cbx)
            base_vbox.addLayout(hbox)

        btn_hbox = QHBoxLayout()
        btn_hbox.addWidget(self.ok_btn)
        btn_hbox.addWidget(self.cancel_btn)

        base_layout = QVBoxLayout()
        base_layout.addLayout(base_vbox)
        base_layout.addLayout(btn_hbox)

        self.setLayout(base_layout)

        self.setWindowTitle("Linux Buddy - Launch Parameters")

    def cbx_state_changed(self):
        sender = self.sender()
        x = self.mapping.get(sender)
        self.launch_settings.__dict__[x] = sender.isChecked()

    def ok_btn_pressed(self):
        self.launch_settings.write(Path(f"~/.linux_buddy/{self.account_name}.json").expanduser().resolve())
        self.close()

    def cancel_btn_pressed(self):
        self.close()
