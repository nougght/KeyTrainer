from PySide6.QtCore import QSettings

class SettingsModel:
    def __init__(self):
        self.settings = QSettings()
    
    def get_theme(self):
        return self.settings.value("theme", "light")
    
    def switch_theme(self):
        self.settings.setValue("theme", "light" if self.get_theme() == "light" else "dark")
    