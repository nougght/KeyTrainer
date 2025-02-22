from PySide6.QtCore import QSettings

class SettingsModel:
    def __init__(self):
        self.settings = QSettings("pyKey", "KeyTrainer")
        print(self.settings.allKeys())

    def get_theme(self):
        return self.settings.value("theme")
    
    def switch_theme(self):
        self.settings.setValue("theme", "dark" if self.get_theme() == "light" else "light")