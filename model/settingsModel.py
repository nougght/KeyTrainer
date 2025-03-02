from PySide6.QtCore import QSettings
from PySide6.QtGui import QIcon
import os, sys

class settingsModel:
    def __init__(self):
        self.settings = QSettings("pyKey", "Key")
        self.settings.setValue("icon_path", "data/keyIc.ico")
        if self.settings.value("theme") == None:
            self.settings.setValue("theme", "light")
            
        print(self.settings.allKeys())

        self.icon = QIcon(self.resource_path(self.settings.value("icon_path")))
        
        with open(self.resource_path("styles/style.qss"), "r") as f:
            self.def_stylesheet = f.read()
        
        with open(self.resource_path("styles/light.qss"), "r") as f:
            self.light_stylesheet = f.read()

        with open(self.resource_path("styles/dark.qss"), "r") as f:
            self.dark_stylesheet = f.read()

    def get_theme(self):
        return self.settings.value("theme")
    def get_icon(self):
        return self.icon
    def get_def_style(self):
        return self.def_stylesheet

    def get_theme_style(self):
        return self.light_stylesheet if self.get_theme() == "light" else self.dark_stylesheet
    
    def switch_theme(self):
        self.settings.setValue("theme", "dark" if self.get_theme() == "light" else "light")

    def resource_path(self, relative_path):
        """Get the absolute path to the resource, works for dev and for PyInstaller"""
        if hasattr(sys, "_MEIPASS"):
            # Если приложение запущено из собранного exe
            base_path = sys._MEIPASS
        else:
            # Если приложение запущено из исходного кода
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)