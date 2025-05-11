from PySide6.QtWidgets import QFrame, QPushButton, QLabel, QComboBox,QMessageBox, QToolButton, QGridLayout, QWidget, QVBoxLayout, QGridLayout, QScrollArea, QSpacerItem, QSizePolicy, QCheckBox
from PySide6.QtCore import Signal, Slot, Qt, QMargins, QPropertyAnimation, Qt
from PySide6.QtGui import QIcon, QAction, QPen, QColor, QPainter

from ui.other_widgets import LoginInput, PasswordInput
from utils import resource_path

class LoginChangeForm(QWidget):
    change_login = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.change_layout = QGridLayout(self)
        self.login_input = LoginInput(placeholderText=self.tr("Новое имя"))
        self.login_input.textChanged.connect(self.switch_login_icon)
        self.change_layout.addWidget(self.login_input, 0, 0, 1, 1)
        self.correct_login_icon = QToolButton()
        self.correct_login_icon.setObjectName('login_change_icon')
        self.switch_login_icon()
        self.change_layout.addWidget(self.correct_login_icon, 0, 1, 1, 1)

        self.change_btn = QPushButton(self.tr("Подтвердить"))
        self.change_btn.clicked.connect(self.on_change_login)
        self.change_layout.addWidget(self.change_btn, 1, 0, 1, 2)

    def switch_login_icon(self):
        if self.login_input.is_correct:
            self.correct_login_icon.setProperty('mode', 'ok')
            self.correct_login_icon.style().unpolish(self.correct_login_icon)  # Обновляем стиль
            self.correct_login_icon.style().polish(self.correct_login_icon)
            self.correct_login_icon.update()
            # self.correct_login_icon.setIcon(QIcon(resource_path("data/checkmark.svg")))
        else:
            self.correct_login_icon.setProperty("mode", "cross")
            self.correct_login_icon.style().unpolish(self.correct_login_icon)  # Обновляем стиль
            self.correct_login_icon.style().polish(self.correct_login_icon)
            self.correct_login_icon.update()

    def on_change_login(self):
        username = self.login_input.text().strip()
        warning0 = self.login_input.warning

        if warning0 is not None:
            QMessageBox.warning(self, self.tr("Ошибка"), warning0)
        else:
            self.change_login.emit(username)
            self.login_input.clear()
            QMessageBox.information(self, "KeyTrainer", self.tr('Имя пользователя успешно изменено'))

            # self.user_combo.setCurrentIndex(self.user_combo.findText(username))
            # print(self.user_combo.findText(username))


class PasswordChangeForm(QWidget):
    password_change_request = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.change_layout = QGridLayout(self)
        self.password_input = PasswordInput(placeholderText=self.tr("Текущий пароль"))
        self.change_layout.addWidget(self.password_input, 0, 0, 1, 2)

        self.new_password_input = PasswordInput(placeholderText=self.tr("Новый пароль"))
        self.new_password_input.textChanged.connect(self.switch_password_icon)
        self.change_layout.addWidget(self.new_password_input, 1, 0, 1, 1)
        self.correct_password_icon = QToolButton()
        self.correct_password_icon.setObjectName('change_password_icon')
        self.switch_password_icon()
        self.change_layout.addWidget(self.correct_password_icon, 1, 1, 1, 1)

        self.password_verify_input = PasswordInput(placeholderText=self.tr("Подтверждение пароля"))
        self.password_verify_input.textChanged.connect(self.switch_verify_icon)
        self.change_layout.addWidget(self.password_verify_input, 2, 0, 1, 1)
        self.correct_verify_icon = QToolButton()
        self.correct_verify_icon.setObjectName('change_verify_icon')
        self.switch_verify_icon()
        self.change_layout.addWidget(self.correct_verify_icon, 2, 1, 1, 1)

        self.change_btn = QPushButton(self.tr("Подтвердить"))
        self.change_btn.clicked.connect(self.on_change_password)
        self.change_layout.addWidget(self.change_btn, 3, 0, 1, 2)

    def switch_password_icon(self):
        if self.new_password_input.is_correct:
            self.correct_password_icon.setProperty('mode', 'ok')
            self.correct_password_icon.style().unpolish(self.correct_password_icon)  # Обновляем стиль
            self.correct_password_icon.style().polish(self.correct_password_icon)
            self.correct_password_icon.update()
            # self.correct_password_icon.setIcon(QIcon(resource_path("data/checkmark.svg")))
        else:
            self.correct_password_icon.setProperty("mode", "cross")
            self.correct_password_icon.style().unpolish(self.correct_password_icon)  # Обновляем стиль
            self.correct_password_icon.style().polish(self.correct_password_icon)
            self.correct_password_icon.update()


    def switch_verify_icon(self):
        if self.password_verify_input.is_correct:
            self.correct_verify_icon.setProperty('mode', 'ok')
            self.correct_verify_icon.style().unpolish(self.correct_verify_icon)  # Обновляем стиль
            self.correct_verify_icon.style().polish(self.correct_verify_icon)
            self.correct_verify_icon.update()
            # self.correct_verify_icon.setIcon(QIcon(resource_path("data/checkmark.svg")))
        else:
            self.correct_verify_icon.setProperty("mode", "cross")
            self.correct_verify_icon.style().unpolish(self.correct_verify_icon)  # Обновляем стиль
            self.correct_verify_icon.style().polish(self.correct_verify_icon)
            self.correct_verify_icon.update()

    def on_change_password(self):
        old_password = self.password_input.text()
        new_password = self.new_password_input.text()
        password_verify = self.password_verify_input.text()

        warning1 = self.new_password_input.warning
        warning2 = self.password_verify_input.warning

        if warning1 is not None:
            QMessageBox.warning(self, self.tr("Ошибка"), warning1)
        elif new_password != password_verify:
            QMessageBox.warning(self, self.tr("Ошибка"), self.tr("Пароли не совпадают"))
        else:
            self.password_change_request.emit(old_password, new_password)
            # self.user_combo.setCurrentIndex(self.user_combo.findText(username))
            # print(self.user_combo.findText(username))

    def on_request_answer(self, is_accepted):
        if is_accepted:
            self.password_input.clear()
            self.new_password_input.clear()
            self.password_verify_input.clear()
            QMessageBox.information(self, "KeyTrainer", self.tr("Пароль успешно изменен"))
        else:
            QMessageBox.warning(self, self.tr('Ошибка'), self.tr('Неправильный пароль'))

# виджет(вкладка) настроек
class SettingsWidget(QFrame):
    user_leaved = Signal()
    user_deleted = Signal()
    change_keyboard_visible = Signal(bool)
    clear_user_data = Signal()
    change_language = Signal(str)
    export_user = Signal()
    import_user = Signal()
    def __init__(self):
        super().__init__()
        self.main_layout = QGridLayout(self)
        self.main_layout.setContentsMargins(100, 20, 100, 20)
        self.main_layout.setHorizontalSpacing(30)
        self.main_layout.setVerticalSpacing(15)
        self.username_change_label = QLabel(self.tr('Сменить имя пользователя'))
        self.main_layout.addWidget(self.username_change_label, 0, 0)
        self.name_change_form = LoginChangeForm()
        self.main_layout.addWidget(self.name_change_form, 0, 1)
        self.password_change_label = QLabel(self.tr('Сменить пароль'))
        self.main_layout.addWidget(self.password_change_label, 1, 0, Qt.AlignmentFlag.AlignLeft)
        self.password_change_form = PasswordChangeForm()
        self.main_layout.addWidget(self.password_change_form, 1, 1)
        self.stats_reset = QPushButton(self.tr('Сбросить статистику профиля'))
        self.stats_reset.clicked.connect(self.on_clear_data)
        self.main_layout.addWidget(self.stats_reset, 2, 0, 1, 2)

        spacer1 = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.main_layout.addItem(spacer1, 3, 0, 1, 2)
        self.language_change_label = QLabel(self.tr('Язык интерфейса'))
        self.main_layout.addWidget(self.language_change_label, 5, 0)

        self.language_combo = QComboBox()
        self.language_combo.addItem(self.tr("Русский"), "ru")
        self.language_combo.addItem(self.tr("Английский"), "en")
        self.language_combo.currentIndexChanged.connect(lambda index: self.change_language.emit(self.language_combo.currentData()))
        self.main_layout.addWidget(self.language_combo, 5, 1, Qt.AlignmentFlag.AlignCenter)

        self.keyboard_visible = QCheckBox(self.tr('Отображать клавиатуру во время тренировки'))
        self.keyboard_visible.setChecked(True)
        self.keyboard_visible.stateChanged.connect(lambda is_visible: self.change_keyboard_visible.emit(is_visible))
        self.main_layout.addWidget(self.keyboard_visible, 4, 0)

        spacer2 = QSpacerItem(
            20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.main_layout.addItem(spacer2, 6, 0, 1, 2)

        self.profile_export = QPushButton(self.tr('Экспорт аккаунта'))
        self.profile_export.clicked.connect(self.export_user.emit)
        self.main_layout.addWidget(self.profile_export, 7, 0, 1, 2)

        self.profile_import = QPushButton(self.tr("Импорт аккаунта"))
        self.profile_import.clicked.connect(self.import_user.emit)
        self.main_layout.addWidget(self.profile_import, 8, 0, 1, 2)

        self.leave_user = QPushButton(self.tr("Выйти из аккаунта"))
        self.leave_user.setObjectName("leave_btn")
        self.leave_user.clicked.connect(self.user_leaved)
        self.main_layout.addWidget(self.leave_user, 9, 0, 1, 2)

        self.delete_user = QPushButton(self.tr("Удалить аккаунт"))
        self.delete_user.setObjectName("delete_btn")
        self.delete_user.clicked.connect(self.on_delete_user)
        self.main_layout.addWidget(self.delete_user, 10, 0, 1, 2)

    def set_lang_combo(self, lang):
        self.language_combo.setCurrentIndex(self.language_combo.findData(lang))

    def on_clear_data(self):
        ret = QMessageBox.warning(self,
            "KeyTrainer",
            self.tr("Все данные будут очищены\nПродолжить?"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,)

        if ret == QMessageBox.StandardButton.Yes:
            self.clear_user_data.emit()

    def on_delete_user(self):
        ret = QMessageBox.warning(self,
            "KeyTrainer",
            self.tr("После удаления все данные будут очищены\nПродолжить?"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,)

        if ret == QMessageBox.StandardButton.Yes:
            self.user_deleted.emit()

    def event(self, event):
        from PySide6.QtCore import QEvent
        if event.type() == QEvent.Type.LanguageChange:
            self.retranslate()
        return super().event(event)

    def retranslate(self):
        self.name_change_form.login_input.setPlaceholderText(self.name_change_form.tr("Новое имя"))
        self.name_change_form.change_btn.setText(self.password_change_form.tr("Подтвердить"))
        self.password_change_form.password_input.setPlaceholderText(self.password_change_form.tr("Текущий пароль"))
        self.password_change_form.new_password_input.setPlaceholderText(self.password_change_form.tr("Новый пароль"))
        self.password_change_form.password_verify_input.setPlaceholderText(self.password_change_form.tr("Подтверждение пароля"))
        self.password_change_form.change_btn.setText(self.password_change_form.tr("Подтвердить"))
        self.username_change_label.setText(self.tr("Сменить имя пользователя"))
        self.password_change_label.setText(self.tr("Сменить пароль"))
        self.stats_reset.setText(self.tr("Сбросить статистику профиля"))
        self.language_change_label.setText(self.tr("Язык интерфейса"))

        self.language_combo.setItemText(0, self.tr("Русский"))
        self.language_combo.setItemText(1, self.tr("Английский"))
        self.keyboard_visible.setText(self.tr('Отображать клавиатуру во время тренировки'))
        self.profile_import.setText(self.tr("Импорт аккаунта"))
        self.profile_export.setText(self.tr("Экспорт аккаунта"))
        self.leave_user.setText(self.tr("Выйти из аккаунта"))
        self.delete_user.setText(self.tr("Удалить аккаунт"))
