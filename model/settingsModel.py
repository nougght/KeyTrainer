from PySide6.QtCore import QSettings
import os, sys
# модель настроек
class settingsModel:
    def __init__(self):
        # инициализация парметров
        self.settings = QSettings("KeyTrainer", "v1.0")
        self.settings.setValue("icon_path", "data/keyIc.ico")
        # self.settings.remove("theme")
        if self.settings.value("theme") not in ["defaultDark", "defaultLight"]:
            self.settings.setValue("theme", "defaultDark")
        if self.settings.value("language") not in ["ru", "en"]:
            self.settings.setValue("language", "en")

        # print(self.settings.allKeys())

        self.styles = {}
        with open(self.resource_path("styles/baseStyle.qss"), "r") as f:
            self.styles['baseStyle'] = f.read()

    def get_theme(self):
        return self.settings.value("theme")
    def get_language(self):
        return self.settings.value("language")

    def get_icon(self):
        return self.icon

    def get_base_style(self):
        return self.styles['baseStyle']

    def get_theme_style(self):
        if self.get_theme() not in self.styles:
            self.load_style(self.get_theme())
        return self.styles[self.get_theme()]

    def switch_theme(self, theme):
        # self.settings.setValue("theme", "defaultDark" if self.get_theme() == "defaultLight" else "defaultLight")
        self.settings.setValue("theme", theme)

    def set_language(self, language):
        self.settings.setValue("language", language)

    def set_last_user(self, user_id):
        self.settings.setValue("user_id", user_id)

    def get_last_user(self):
        id = self.settings.value("user_id")
        return id if id else 0
    
    # загрузка стилей из файлов
    def load_style(self, name):
        lst = []
        with open(self.resource_path(f"styles/{name}/widgetStyle.qss"), "r") as f:
            lst.append(f.read())
        with open(self.resource_path(f"styles/{name}/textStyle.qss"), "r") as f:
            lst.append(f.read())
        self.styles[name] = lst

    # функция получения пути к файлу в собранном проекте
    def resource_path(self, relative_path):
        if hasattr(sys, "_MEIPASS"):
            # Если приложение запущено из собранного exe
            base_path = sys._MEIPASS
        else:
            # Если приложение запущено из исходного кода
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
