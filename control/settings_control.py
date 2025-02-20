from model.settingsModel import SettingsModel
from PySide6.QtCore import Signal

class SettingControl:
    theme_changed = Signal(str)
    def __init__(self):
        self.model = SettingsModel()
    
    def on_theme_change(self):
        self.model.switch_theme()
        self.theme_changed.emit(self.model.get_theme())