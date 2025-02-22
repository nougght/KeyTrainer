from PySide6.QtCore import QObject
from model import profilesMode,settingsModel, wordListModel.wordListModel, textListModel.textListModel
class MainControl(QObject):
    def __init__(self):
        self.text_list_model = TextCollectionModel()
        self.word_list_model = WordListModel()
        self.statistics_model = StatisticsModel()
        self.profile_model = ProfileModel()

        self.main_window = MainWindow()
        self.start_window = StartWindow()
        # self.statistics_view = StatisticsView()
