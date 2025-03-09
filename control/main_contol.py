from PySide6.QtCore import QObject
from PySide6.QtWidgets import QDialog
from model import settingsModel, statisticsModel, ProfilesList, WordList, TextList

from ui.main_win import MainWindow
from ui.my_widgets import StarterDialog, KeyWidget
from control import TypingControl, SettingControl
import sys

class mainControl(QObject):
    def __init__(self):
        self.settings_model = settingsModel()
        self.statistics_model = statisticsModel()
        self.text_list_model = TextList()
        self.word_list_model = WordList()
        self.profile_model = ProfilesList()

        self.main_window = MainWindow()
        self.start_window = StarterDialog()
        # self.statistics_view = StatisticsView()

        self.typing_control = TypingControl(self.text_list_model, self.word_list_model, self.main_window)
        self.setting_control = SettingControl(self.settings_model, self.main_window, self.start_window)
        # self.statistics_control = StatisticsController(self.statistics_model, self.statistics_view)
        # self.profile_controller = ProfileController(self.profile_model, self.start_window_view)

        KeyWidget.style[0], KeyWidget.style[1] = (
            (KeyWidget.style[1], KeyWidget.style[0])
            if self.settings_model.get_theme() == "dark"
            else (KeyWidget.style[0], KeyWidget.style[1])
        )

    def show_starter_window(self):
        if self.start_window.exec() == QDialog.Accepted:
            self.main_window.showMaximized()
            self.main_window.text_display.setFocus()
        else:
            sys.exit()
            

    def start_new_session(self, profile_name):
        self.profile_controller.load_profile(profile_name)
        self.main_window_view.show()
