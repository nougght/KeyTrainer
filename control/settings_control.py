import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from model.settingsModel import SettingsModel
from PySide6 import QtCore
from PySide6.QtCore import Signal

class SettingControl(QtCore.QObject):
    theme_changed = Signal(str)
    def __init__(self, settings_model):
        super().__init__()
        self.model = settings_model
    
    def on_theme_change(self):
        self.model.switch_theme()
        self.theme_changed.emit(self.model.get_theme())

m = SettingsModel()
s = SettingControl(m)
print(s.model.get_theme())
s.on_theme_change()
print(s.model.get_theme())
