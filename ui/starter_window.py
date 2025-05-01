# views/login_window.py
from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QComboBox,
    QPushButton,
    QLineEdit,
    QMessageBox,
)
from control.users_control import UserController


class LoginWindow(QDialog):
    user_selected = Signal(int)
    create_new_user = Signal(str)

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Вход")
        layout = QVBoxLayout()

        self.user_combo = QComboBox()
        layout.addWidget(self.user_combo)

        self.new_user_input = QLineEdit(placeholderText="Новый пользователь")
        layout.addWidget(self.new_user_input)

        self.create_btn = QPushButton("Создать", clicked=self.on_create_user)
        layout.addWidget(self.create_btn)

        self.login_btn = QPushButton("Войти")
        self.login_btn.clicked.connect(self.on_login)
        layout.addWidget(self.login_btn)

        self.setLayout(layout)

    def show_users(self, users):
        """Загружает пользователей через контроллер."""
        self.user_combo.clear()
        for user in users:
            self.user_combo.addItem(user["username"], user["id"])

    def on_create_user(self):
        """Обработчик создания пользователя."""
        username = self.new_user_input.text().strip()
        if not username:
            QMessageBox.warning(self, "Ошибка", "Имя не может быть пустым")
            return

        self.create_new_user.emit(username)
        self.user_combo.setCurrentIndex(self.user_combo.findText(username))
        print(self.user_combo.findText(username))
        self.new_user_input.clear()

        # QMessageBox.warning(self, "Ошибка", "Пользователь уже существует")
    def on_login(self):
        user_id = self.user_combo.currentData()
        if user_id:
            self.user_selected.emit(user_id)
            self.accept()
