from PySide6.QtCore import QSettings
from PySide6.QtGui import QIcon
import os, sys

class settingsModel:
    def __init__(self):
        self.settings = QSettings("pyKey", "KeyTrainer0.3")
        self.settings.setValue("icon_path", "data/keyIc.ico")
        if (self.settings.value("theme") == None):
            self.settings.setValue("theme", "defaultDark")
        print(self.settings.allKeys())

        self.icon = QIcon(self.resource_path(self.settings.value("icon_path")))

        self.styles = {}
        with open(self.resource_path("styles/baseStyle.qss"), "r") as f:
            self.styles['baseStyle'] = f.read()


    def get_theme(self):
        return self.settings.value("theme")
    def get_icon(self):
        return self.icon
    def get_base_style(self):
        return self.styles['baseStyle']

    def get_theme_style(self):
        if self.get_theme() not in self.styles:
            self.load_style(self.get_theme())
        return self.styles[self.get_theme()]

    def switch_theme(self):
        self.settings.setValue("theme", "defaultDark" if self.get_theme() == "defaultLight" else "defaultLight")

    def load_style(self, name):
        lst = []
        with open(self.resource_path(f"styles\{name}\widgetStyle.qss"), "r") as f:
            lst.append(f.read())
        with open(self.resource_path(f"styles/{name}/textStyle.qss"), "r") as f:
            lst.append(f.read())
        self.styles[name] = lst

    def resource_path(self, relative_path):
        """Get the absolute path to the resource, works for dev and for PyInstaller"""
        if hasattr(sys, "_MEIPASS"):
            # Если приложение запущено из собранного exe
            base_path = sys._MEIPASS
        else:
            # Если приложение запущено из исходного кода
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
