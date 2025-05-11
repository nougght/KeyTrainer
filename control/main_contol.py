from PySide6.QtCore import QObject, Qt, QDate 
from PySide6.QtWidgets import QDialog
from model import dataBase, TextRepository, settingsModel, UserSession, UserRepository, SessionRepository, TimePointsRepository, DailyActivityRepository
from control import TypingControl, SettingControl, UserController, StatisticsControl
from ui.main_window import MainWindow
from ui.starter_window import LoginWindow
import sys

# основной контроллер - инициализирует и связывает остальные части приложения
class mainControl(QObject):
    def __init__(self):

        self.data_base = dataBase.Database('data/data.db')

        # модели - репозитории для каждой таблицы бд
        self.text_repository = TextRepository(self.data_base)
        self.user_repository = UserRepository(self.data_base)
        self.session_repository = SessionRepository(self.data_base)
        self.time_points_repository = TimePointsRepository(self.data_base)
        self.daily_activity_repository = DailyActivityRepository(self.data_base)
        # модель настроек QSettings
        self.settings_model = settingsModel()
        # текущий пользователь приложения
        self.user_session = UserSession()

        # стартовое окно
        self.start_window = LoginWindow()
        # основное окно
        self.main_window = MainWindow()

        # контроллеры - связывают представление(интерфейс) с моделям(данными)
        self.user_control = UserController(self.start_window, self.main_window, self.user_repository, self.user_session)
        self.statistics_control = StatisticsControl(self.text_repository, self.user_repository, self.session_repository, self.time_points_repository, self.daily_activity_repository, self.main_window, self.user_session)
        self.typing_control = TypingControl(self.text_repository, self.main_window)
        self.typing_control.typing_stats.connect(lambda a, b, data : self.statistics_control.on_session_finished(data))
        self.setting_control = SettingControl(self.settings_model, self.main_window, self.start_window)
        
        self.user_control.successful_login.connect(self.setting_control.set_user)
        self.user_control.user_created.connect(self.setting_control.set_user)
        self.main_window.settings_widget.name_change_form.change_login.connect(self.user_control.change_username)
        self.main_window.settings_widget.name_change_form.change_login.connect(lambda: self.statistics_control.show_general_stats(self.user_session.get_uid()))
        self.main_window.settings_widget.user_leaved.connect(self.return_to_login)

        self.main_window.settings_widget.password_change_form.password_change_request.connect(self.user_control.handle_password_change)
        self.main_window.settings_widget.user_deleted.connect(self.statistics_control.delete_current_user)
        self.main_window.settings_widget.user_deleted.connect(self.return_to_login)
        self.start_window.import_user.connect(self.statistics_control.import_user)
    # выход из основного окна в окну входа
    def return_to_login(self):
        self.main_window.close()
        self.start_window.show_users(self.user_control.get_all_users())
        self.show_starter_window()
    # показ окна входа и запуск основного
    def show_starter_window(self):
        if self.user_control.get_all_users():
            self.start_window.stack.setCurrentIndex(0)
        else:
            self.start_window.stack.setCurrentIndex(1)
        self.start_window.show()
        if self.start_window.exec() == QDialog.DialogCode.Accepted:
            # после выбора входа пользователя - получение данных из бд
            self.user_repository.recalculate_user_data(
                self.user_session.get_user()["user_id"]
            )
            for i in range(366):
                self.statistics_control.daily_activity_repository.recalculate_activity(self.user_session.get_uid(), (QDate.currentDate().addDays(-i).toString("yyyy-MM-dd")))

            self.statistics_control.show_general_stats(self.user_session.get_user()["user_id"])
            self.main_window.setWindowFlags(
                Qt.WindowType.FramelessWindowHint  # Убираем рамку основного окна
            )

            self.main_window.showMaximized() # на весь экран
            self.main_window.tab.tabBar.setCurrentIndex(0)
            self.main_window.typing_widget.text_display.setFocus()
        else:
            sys.exit() # выхода из приложения если начальное окно было закрыто

