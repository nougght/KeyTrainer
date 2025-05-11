# views/login_window.py
from PySide6.QtCore import Slot, Signal, Qt, QRegularExpression, QEvent
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QComboBox,
    QPushButton,
    QLineEdit,
    QMessageBox,
    QWidget,
    QLabel,
    QGridLayout,
    QCheckBox,
    QStackedLayout,
    QToolButton
)
from PySide6.QtGui import QRegularExpressionValidator, QAction, QIcon
from control.users_control import UserController
from ui.other_widgets import LoginInput, PasswordInput, ThemeButton
from utils import resource_path


class LoginForm(QWidget):
    to_registration = Signal()
    to_recovery = Signal()
    user_login_request = Signal(int, str)
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.login_layout = QVBoxLayout(self)
        self.login_layout.setSpacing(7)
        self.login_layout.setContentsMargins(15, 15, 15, 15)

        self.login_label = QLabel(self.tr('Вход'))
        self.login_layout.addWidget(self.login_label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.user_combo = QComboBox()
        self.login_layout.addWidget(self.user_combo)
        self.password_input = PasswordInput(placeholderText=self.tr("Пароль"))
        self.login_layout.addWidget(self.password_input)
        self.login_btn = QPushButton(self.tr("Войти"))
        self.login_btn.clicked.connect(self.on_login)
        self.login_layout.addWidget(self.login_btn)

        self.login_to_registration = QPushButton(self.tr("Регистрация"))
        self.login_to_registration.setObjectName("to_registration")
        self.login_to_registration.clicked.connect(self.to_registration)
        self.login_layout.addWidget(self.login_to_registration)
        self.password_recovery = QPushButton(self.tr("Забыли пароль?"))
        self.password_recovery.setObjectName("to_password_recovery")
        self.password_recovery.clicked.connect(self.to_recovery.emit)
        self.login_layout.addWidget(self.password_recovery)

        self.profile_import = QPushButton(self.tr("Импорт аккаунта"))
        self.login_layout.addWidget(self.profile_import)

    def set_last_user(self, user_id):
        self.user_combo.setCurrentIndex(self.user_combo.findData(user_id))

    def on_login(self):
        user_id = self.user_combo.currentData()
        if user_id:
            self.user_login_request.emit(user_id, self.password_input.text())


class RegistrationForm(QWidget):
    to_login = Signal()
    create_new_user = Signal(str, str, str)
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.registration_layout = QGridLayout(self)
        self.registration_layout.setSpacing(7)
        self.registration_layout.setContentsMargins(15, 15, 15, 15)
        self.registration_label = QLabel(self.tr("Регистрация"))
        self.registration_layout.addWidget(
            self.registration_label, 0, 0, 1, 2,
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter,
        )
        self.login_input = LoginInput(placeholderText=self.tr("Имя пользователя"))
        self.login_input.textChanged.connect(self.switch_login_icon)
        self.registration_layout.addWidget(self.login_input, 1, 0, 1, 1)
        self.correct_login_icon = QToolButton()
        self.correct_login_icon.setObjectName('reg_login_icon')

        self.switch_login_icon()
        self.registration_layout.addWidget(self.correct_login_icon, 1, 1, 1, 1)

        self.password_input = PasswordInput(placeholderText=self.tr("Пароль"))
        self.password_input.textChanged.connect(self.switch_password_icon)
        self.registration_layout.addWidget(self.password_input, 2, 0, 1, 1)
        self.correct_password_icon = QToolButton()
        self.correct_password_icon.setObjectName("reg_password_icon")
        self.switch_password_icon()
        self.registration_layout.addWidget(self.correct_password_icon, 2, 1, 1, 1)

        self.password_verify_input = PasswordInput(placeholderText=self.tr("Подтверждение пароля"))
        self.password_verify_input.textChanged.connect(self.switch_verify_icon)
        self.registration_layout.addWidget(self.password_verify_input, 3, 0, 1, 1)
        self.correct_verify_icon = QToolButton()
        self.correct_verify_icon.setObjectName("reg_verify_icon")
        self.switch_verify_icon()
        self.registration_layout.addWidget(self.correct_verify_icon)

        self.recovery_input = PasswordInput(placeholderText=self.tr("Код для восстановления"))
        self.registration_layout.addWidget(self.recovery_input, 4, 0, 1, 1)

        self.registration_btn = QPushButton(self.tr("Зарегистрироваться"))
        self.registration_btn.clicked.connect(self.on_create_user)
        self.registration_layout.addWidget(self.registration_btn, 5, 0, 1, 2)

        self.registration_to_login = QPushButton(self.tr("Вход"))
        self.registration_to_login.setObjectName("to_login")
        self.registration_to_login.clicked.connect(self.to_login)
        self.registration_layout.addWidget(self.registration_to_login, 6, 0, 1, 2)
        self.password_checkbox = QCheckBox(self.tr("Использовать пароль?"))
        self.password_checkbox.setChecked(True)
        self.password_checkbox.stateChanged.connect(lambda: self.on_password_enable(self.password_checkbox.isChecked()))
        self.registration_layout.addWidget(self.password_checkbox, 7, 0, 1, 2)

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
        # self.correct_login_icon.setIcon(QIcon(resource_path("data/cross.svg")))

    def switch_password_icon(self):
        if self.password_input.is_correct:
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
        else:
            self.correct_verify_icon.setProperty("mode", "cross")
            self.correct_verify_icon.style().unpolish(self.correct_verify_icon)  # Обновляем стиль
            self.correct_verify_icon.style().polish(self.correct_verify_icon)
            self.correct_verify_icon.update()

    def on_password_enable(self, is_enable):
        if is_enable:
            self.password_input.setEnabled(True)
            self.password_verify_input.setEnabled(True)
        else:
            self.password_input.setEnabled(False)
            self.password_verify_input.setEnabled(False)

    def on_create_user(self):
        """Обработчик создания пользователя."""
        username = self.login_input.text().strip()
        is_password_enabled = self.password_checkbox.isChecked()
        password = self.password_input.text().strip()
        password_verify = self.password_verify_input.text().strip()
        recovery_code = self.recovery_input.text().strip()
        warning0 = self.login_input.warning
        warning1 = self.password_input.warning
        warning2 = self.password_verify_input.warning

        if warning0 is not None:
            QMessageBox.warning(self, self.tr("Ошибка"), warning0)
        elif is_password_enabled:
            if warning1 is not None:
                QMessageBox.warning(self, self.tr("Ошибка"), warning1)
            elif password != password_verify:
                QMessageBox.warning(self, self.tr("Ошибка"), self.tr("Пароли не совпадают"))
            else:
                self.create_new_user.emit(username, password, recovery_code)
        else:
            self.create_new_user.emit(username, password, recovery_code)
            # self.user_combo.setCurrentIndex(self.user_combo.findText(username))
            # print(self.user_combo.findText(username))


class PasswordRecoveryForm(QWidget):
    password_recovery_request = Signal(int, str, str)
    recovery_to_login = Signal()
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.change_layout = QGridLayout(self)

        self.recovery_label = QLabel(self.tr("Восстановление"))
        self.change_layout.addWidget(
            self.recovery_label, 0, 0, 1, 2,
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter,
        )

        self.user_combo = QComboBox()
        self.change_layout.addWidget(self.user_combo, 1, 0, 1, 2)

        self.code_input = PasswordInput(placeholderText=self.tr("Код восставновления"))
        self.change_layout.addWidget(
            self.code_input, 2, 0, 1, 2, Qt.AlignmentFlag.AlignTop
        )

        self.new_password_input = PasswordInput(placeholderText=self.tr("Новый пароль"))
        self.new_password_input.textChanged.connect(self.switch_password_icon)
        self.change_layout.addWidget(
            self.new_password_input, 3, 0, 1, 1, Qt.AlignmentFlag.AlignTop
        )
        self.correct_password_icon = QToolButton()
        self.correct_password_icon.setObjectName('rec_password_icon')
        self.switch_password_icon()
        self.change_layout.addWidget(
            self.correct_password_icon, 3, 1, 1, 1, Qt.AlignmentFlag.AlignTop
        )

        self.password_verify_input = PasswordInput(
            placeholderText=self.tr("Подтверждение пароля")
        )
        self.password_verify_input.textChanged.connect(self.switch_verify_icon)
        self.change_layout.addWidget(
            self.password_verify_input, 4, 0, 1, 1, Qt.AlignmentFlag.AlignTop
        )
        self.correct_verify_icon = QToolButton()
        self.correct_verify_icon.setObjectName("rec_verify_icon")
        self.switch_verify_icon()
        self.change_layout.addWidget(
            self.correct_verify_icon, 4, 1, 1, 1, Qt.AlignmentFlag.AlignTop
        )

        self.change_btn = QPushButton(self.tr("Восстановить"))
        self.change_btn.clicked.connect(self.on_recover_password)
        self.change_layout.addWidget(
            self.change_btn, 5, 0, 1, 2, Qt.AlignmentFlag.AlignTop
        )

        self.to_login = QPushButton(self.tr("Вход"))
        self.to_login.setObjectName("to_login")
        self.to_login.clicked.connect(self.recovery_to_login)
        self.change_layout.addWidget(self.to_login, 6, 0, 1, 2)

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

    def on_recover_password(self):
        user_id = self.user_combo.currentData()
        code = self.code_input.text()
        new_password = self.new_password_input.text()
        password_verify = self.password_verify_input.text()

        warning1 = self.new_password_input.warning
        warning2 = self.password_verify_input.warning

        if warning1 is not None:
            QMessageBox.warning(self, self.tr("Ошибка"), warning1)
        elif new_password != password_verify:
            QMessageBox.warning(self, self.tr("Ошибка"), self.tr("Пароли не совпадают"))
        else:
            self.password_recovery_request.emit(user_id, code, new_password)
            # self.user_combo.setCurrentIndex(self.user_combo.findText(username))
            # print(self.user_combo.findText(username))

    def on_request_answer(self, is_accepted):
        if is_accepted:
            self.code_input.clear()
            self.new_password_input.clear()
            self.password_verify_input.clear()
            QMessageBox.information(self, "KeyTrainer", self.tr("Пароль успешно изменен"))
        else:
            QMessageBox.warning(self, self.tr("Ошибка"), self.tr("Неправильный пароль"))


class LoginWindow(QDialog):
    change_language = Signal(str)
    change_theme = Signal(str)
    import_user = Signal()
    update_user = Signal()
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setFixedWidth(400)
        self.setWindowTitle(self.tr("Авторизация"))
        self.main_layout = QGridLayout(self)
        self.main_layout.setSpacing(15)
        self.stack = QStackedLayout()
        self.main_layout.addLayout(self.stack, 0, 0, 1, 2)
        self.style_btn = ThemeButton()
        self.style_btn.theme_changed.connect(lambda t: self.change_theme.emit(t))
        self.language_combo = QComboBox()
        self.language_combo.addItem(self.tr("Русский"), "ru")
        self.language_combo.addItem(self.tr("Английский"), "en")

        self.language_combo.currentIndexChanged.connect(lambda index: self.change_language.emit(self.language_combo.currentData()))
        self.main_layout.addWidget(self.style_btn, 1, 0)
        self.main_layout.addWidget(self.language_combo, 1, 1)

        self.login_form = LoginForm()

        self.registration_form = RegistrationForm()

        self.recovery_form = PasswordRecoveryForm()

        self.stack.addWidget(self.login_form)
        self.stack.addWidget(self.registration_form)
        self.stack.addWidget(self.recovery_form)
        self.login_form.to_registration.connect(lambda: self.switch_form(1))
        self.login_form.to_recovery.connect(lambda: (self.switch_form(2), self.adjustSize()))
        self.registration_form.to_login.connect(lambda: (self.switch_form(0)))
        self.recovery_form.recovery_to_login.connect(lambda: self.switch_form(0))
        self.registration_form.create_new_user.connect(self.accept)
        self.login_form.profile_import.clicked.connect(lambda: (self.import_user.emit(),self.update_user.emit()))

        self.stack.setCurrentWidget(self.registration_form)

    def switch_form(self, index):
        self.stack.setCurrentIndex(index)

    def set_lang_combo(self, lang):
        self.language_combo.setCurrentIndex(self.language_combo.findData(lang))

    def show_users(self, users):
        """Загружает пользователей через контроллер."""
        self.login_form.user_combo.clear()
        for user in users:
            self.login_form.user_combo.addItem(user["username"], user["id"])
            self.recovery_form.user_combo.addItem(user["username"], user["id"])
        self.registration_form.login_input.set_used_names([user["username"] for user in users])
        self.update()
        # QMessageBox.warning(self, "Ошибка", "Пользователь уже существует")

    def show_warning(self):
        QMessageBox.warning(self, self.tr('Ошибка'), self.tr('Неправильный пароль'))

    def event(self, event):
        if event.type() == QEvent.Type.LanguageChange:
            self.retranslate()
        return super().event(event)

    def retranslate(self):
        self.login_form.login_label.setText(self.tr("Вход"))
        self.login_form.password_input.setPlaceholderText(self.tr("Пароль"))

        self.login_form.login_btn.setText(self.tr("Войти"))
        self.login_form.login_to_registration.setText(self.tr("Регистрация"))
        self.login_form.password_recovery.setText(self.tr("Забыли пароль?"))
        self.login_form.profile_import.setText(self.tr("Импорт аккаунта"))

        self.registration_form.registration_label.setText(self.tr("Регистрация"))
        self.registration_form.login_input.setPlaceholderText(self.tr("Имя пользователя"))
        self.registration_form.password_input.setPlaceholderText(self.tr("Пароль"))
        self.registration_form.password_verify_input.setPlaceholderText(
            self.tr("Подтверждение пароля")
        )
        self.registration_form.recovery_input.setPlaceholderText(self.tr("Код для восстановления"))
        self.registration_form.registration_btn.setText(self.tr("Зарегистрироваться"))
        self.registration_form.registration_to_login.setText(self.tr("Вход"))
        self.registration_form.password_checkbox.setText(
            self.tr("Использовать пароль?")
        )

        self.recovery_form.recovery_label.setText(self.tr("Восстановление"))
        self.recovery_form.code_input.setPlaceholderText(self.tr("Код восставновления"))
        self.recovery_form.new_password_input.setPlaceholderText(self.tr("Новый пароль"))
        self.recovery_form.password_verify_input.setPlaceholderText(
            self.tr("Подтверждение пароля")
        )
        self.recovery_form.change_btn.setText(self.tr("Восстановить"))
        self.recovery_form.to_login.setText(self.tr("Вход"))

        self.setWindowTitle(self.tr("Авторизация"))
        self.language_combo.setItemText(0, self.tr("Русский"))
        self.language_combo.setItemText(1, self.tr("Английский"))
