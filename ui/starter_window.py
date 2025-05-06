# views/login_window.py
from PySide6.QtCore import Slot, Signal, Qt, QRegularExpression
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
    user_login_request = Signal(int, str)
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.login_layout = QVBoxLayout(self)
        self.login_label = QLabel('Вход')
        self.login_layout.addWidget(self.login_label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.user_combo = QComboBox()
        self.login_layout.addWidget(self.user_combo)
        self.password_input = PasswordInput(placeholderText="Пароль")
        self.login_layout.addWidget(self.password_input)
        self.login_btn = QPushButton("Войти")
        self.login_btn.clicked.connect(self.on_login)
        self.login_layout.addWidget(self.login_btn)

        self.login_to_registration = QPushButton("Регистрация")
        self.login_to_registration.setObjectName("to_registration")
        self.login_to_registration.clicked.connect(self.to_registration)
        self.login_layout.addWidget(self.login_to_registration)
        self.password_recovery = QPushButton("Забыли пароль?")
        self.password_recovery.setObjectName("to_password_recovery")
        self.login_layout.addWidget(self.password_recovery)
    def set_last_user(self, user_id):
        self.user_combo.setCurrentIndex(self.user_combo.findData(user_id))

    def on_login(self):
        user_id = self.user_combo.currentData()
        if user_id:
            self.user_login_request.emit(user_id, self.password_input.text())


class RegistrationForm(QWidget):
    to_login = Signal()
    create_new_user = Signal(str, str)
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.registration_layout = QGridLayout(self)
        self.registration_label = QLabel("Регистрация")
        self.registration_layout.addWidget(
            self.registration_label, 0, 0, 1, 2,
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter,
        )
        self.login_input = LoginInput(placeholderText="Логин")
        self.login_input.textChanged.connect(self.switch_login_icon)
        self.registration_layout.addWidget(self.login_input, 1, 0, 1, 1)
        self.correct_login_icon = QToolButton()
        self.switch_login_icon()
        self.registration_layout.addWidget(self.correct_login_icon, 1, 1, 1, 1)

        self.password_input = PasswordInput(placeholderText="Пароль")
        self.password_input.textChanged.connect(self.switch_password_icon)
        self.registration_layout.addWidget(self.password_input, 2, 0, 1, 1)
        self.correct_password_icon = QToolButton()
        self.switch_password_icon()
        self.registration_layout.addWidget(self.correct_password_icon, 2, 1, 1, 1)

        self.password_verify_input = PasswordInput(placeholderText="Подтверждение пароля")
        self.password_verify_input.textChanged.connect(self.switch_verify_icon)
        self.registration_layout.addWidget(self.password_verify_input, 3, 0, 1, 1)
        self.correct_verify_icon = QToolButton()
        self.switch_verify_icon()
        self.registration_layout.addWidget(self.correct_verify_icon)

        self.registration_btn = QPushButton("Зарегистрироваться")
        self.registration_btn.clicked.connect(self.on_create_user)
        self.registration_layout.addWidget(self.registration_btn, 4, 0, 1, 2)

        self.registration_to_login = QPushButton("Вход")
        self.registration_to_login.setObjectName("to_login")
        self.registration_to_login.clicked.connect(self.to_login)
        self.registration_layout.addWidget(self.registration_to_login, 5, 0, 1, 2)
        self.password_checkbox = QCheckBox("Использовать пароль?")
        self.password_checkbox.setChecked(True)
        self.password_checkbox.stateChanged.connect(lambda: self.on_password_enable(self.password_checkbox.isChecked()))
        self.registration_layout.addWidget(self.password_checkbox, 6, 0, 1, 2)

    def switch_login_icon(self):
        if self.login_input.is_correct:
            self.correct_login_icon.setIcon(QIcon(resource_path("data/checkmark.svg")))
        else:
            self.correct_login_icon.setIcon(QIcon(resource_path("data/cross.svg")))

    def switch_password_icon(self):
        if self.password_input.is_correct:
            self.correct_password_icon.setIcon(QIcon(resource_path("data/checkmark.svg")))
        else:
            self.correct_password_icon.setIcon(QIcon(resource_path("data/cross.svg")))

    def switch_verify_icon(self):
        if self.password_verify_input.is_correct:
            self.correct_verify_icon.setIcon(QIcon(resource_path("data/checkmark.svg")))
        else:
            self.correct_verify_icon.setIcon(QIcon(resource_path("data/cross.svg")))

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
        warning0 = self.login_input.warning
        warning1 = self.password_input.warning
        warning2 = self.password_verify_input.warning

        if warning0 is not None:
            QMessageBox.warning(self, "Ошибка", warning0)
        elif is_password_enabled:
            if warning1 is not None:
                QMessageBox.warning(self, "Ошибка", warning1)
            elif password != password_verify:
                QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
            else:
                self.create_new_user.emit(username, password)
        else:
            self.create_new_user.emit(username, password)
            # self.user_combo.setCurrentIndex(self.user_combo.findText(username))
            # print(self.user_combo.findText(username))


class LoginWindow(QDialog):
    change_theme = Signal(str)
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Авторизация")
        self.main_layout = QGridLayout(self)
        self.stack = QStackedLayout()
        self.main_layout.addLayout(self.stack, 0, 0, 1, 2)
        self.style_btn = ThemeButton()
        self.style_btn.theme_changed.connect(lambda t: self.change_theme.emit(t))
        self.language_btn = QPushButton('ru')
        self.main_layout.addWidget(self.style_btn, 1, 0)
        self.main_layout.addWidget(self.language_btn, 1, 1)

        self.login_form = LoginForm()

        self.registration_form = RegistrationForm()

        self.stack.addWidget(self.login_form)
        self.stack.addWidget(self.registration_form)

        self.login_form.to_registration.connect(lambda: self.switch_form(1))
        self.registration_form.to_login.connect(lambda: self.switch_form(0))

        self.registration_form.create_new_user.connect(self.accept)

    def switch_form(self, index):
        self.stack.setCurrentIndex(index)

    def show_users(self, users):
        """Загружает пользователей через контроллер."""
        self.login_form.user_combo.clear()
        for user in users:
            self.login_form.user_combo.addItem(user["username"], user["id"])
        self.registration_form.login_input.set_used_names([user["username"] for user in users])

        # QMessageBox.warning(self, "Ошибка", "Пользователь уже существует")

    def show_warning(self):
        QMessageBox.warning(self, 'Ошибка', 'Неправильный пароль')
