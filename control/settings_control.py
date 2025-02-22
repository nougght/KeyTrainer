import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget


class SettingControl(QtCore.QObject):
    theme_changed = Signal(str)
    def __init__(self, settings_model, main_window, start_window):
        super().__init__()
        self.model = settings_model

        start_window.setStyleSheet(self.model.get_theme_style())
        main_window.setStyleSheet(self.model.get_theme_style())
        start_window.theme_switch_button.clicked.connect(self.on_theme_change)
        main_window.theme_switch_button.clicked.connect(self.on_theme_change)
        self.theme_changed.connect(start_window.setStyleSheet)
        self.theme_changed.connect(main_window.setStyleSheet)

    def on_theme_change(self):
        self.model.switch_theme()
        self.theme_changed.emit(self.model.get_theme_style())

    def set_def_style(self, wid: QWidget):
        wid.setStyleSheet(self.model.get_def_style())

    def set_light_style(self, wid: QWidget):
        wid.setStyleSheet(self.model.get_light_style())

    def set_dark_style(self, wid: QWidget):
        wid.setStyleSheet(self.model.get_dark_style())
