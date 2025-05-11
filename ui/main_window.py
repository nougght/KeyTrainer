from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, QApplication, QStackedWidget)
from ui.other_widgets import TabBarWithControl
from ui.typing_widget import TypingWidget
from ui.statistics_widget import StatisticsWidget
from ui.settings_widget import SettingsWidget
from PySide6.QtCore import Signal, QEvent


# основное окно с переключением вкладок
class MainWindow(QMainWindow):
    change_theme = Signal(str)
    def __init__(self):
        super().__init__()
        # self.setFixedSize(500, 500)
        self.setWindowTitle("Key Trainer")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.setContentsMargins(0,0,0,0)
        self.central_layout.setSpacing(0)
        # кастомный виджет - верхняя панель с вкладками с кнопками управления окном
        self.tab = TabBarWithControl()
        self.tab.theme_button.theme_changed.connect(lambda t: self.change_theme.emit(t))

        self.tab.minimise_btn.clicked.connect(self.showMinimized)
        self.tab.close_btn.clicked.connect(self.on_exit_released)
        # добавление вкладок
        self.tab.tabBar.addTab(self.tr("Тренировка"))
        self.tab.tabBar.addTab(self.tr("Статистика"))
        self.tab.tabBar.addTab(self.tr("Настройки"))
        self.stacked_widget = QStackedWidget()
        self.typing_widget = TypingWidget()
        self.statistics_widget = StatisticsWidget()
        self.settings_widget = SettingsWidget()
        self.settings_widget.change_keyboard_visible.connect(self.typing_widget.set_keyboard_visible)
        self.stacked_widget.addWidget(self.typing_widget)
        self.stacked_widget.addWidget(self.statistics_widget)
        self.stacked_widget.addWidget(self.settings_widget)

        self.tab.tabBar.currentChanged.connect(self.stacked_widget.setCurrentIndex)
        self.central_layout.addWidget(self.tab)
        self.central_layout.addWidget(self.stacked_widget)
        # self.tab.setStyleSheet('background: green;')

    def setWindowStyle(self, style):
        self.typing_widget.text_display.document().setDefaultStyleSheet(style[1])
        self.typing_widget.text_display.setHtmlText()
        self.setStyleSheet(style[0])
        # print(styleSheet)

    def on_exit_released(self):
        # print("exit")
        self.close()

    def keyPressEvent(self, event):
        from PySide6.QtCore import Qt
        if event.key() == Qt.Key.Key_F11: # убрать панель задач на F11
            if self.isFullScreen():
                self.setWindowState(Qt.WindowState.WindowMaximized)  # Плавный переход
            else:
                self.setWindowState(Qt.WindowState.WindowFullScreen)
        return super().keyPressEvent(event)

    def event(self, event):
        if event.type() == QEvent.Type.LanguageChange:
            self.retranslate()
        return super().event(event)

    def retranslate(self):
        self.tab.tabBar.setTabText(0, self.tr("Тренировка"))
        self.tab.tabBar.setTabText(1, self.tr("Статистика"))
        self.tab.tabBar.setTabText(2, self.tr("Настройки"))


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.showMaximized()

    app.exec()
