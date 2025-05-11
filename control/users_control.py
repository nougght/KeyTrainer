# controllers/user_controller.py
from model import UserRepository
from argon2 import PasswordHasher, exceptions
from PySide6.QtCore import QObject, Signal

# контроллер пользователей
class UserController(QObject):
    user_created = Signal(int)
    successful_login = Signal(int)
    unsuccessful_login = Signal(int)
    password_change_request_answer = Signal(bool)
    password_recovery_request_answer = Signal(bool)

    def __init__(self, login_window, main_window, user_repo, user_session):
        super().__init__()
        self.password_hasher = PasswordHasher()
        self.user_session = user_session
        self.login_window = login_window
        self.user_repo = user_repo  # Зависимость от репозитория

        self.login_window.show_users(self.get_all_users())

        self.login_window.registration_form.create_new_user.connect(self.create_user)
        self.login_window.login_form.user_login_request.connect(self.handle_login)
        self.login_window.recovery_form.password_recovery_request.connect(self.handle_password_recovery)
        self.successful_login.connect(self.login_window.accept)
        self.unsuccessful_login.connect(self.login_window.show_warning)
        self.password_change_request_answer.connect(main_window.settings_widget.password_change_form.on_request_answer)
        self.password_recovery_request_answer.connect(self.login_window.recovery_form.on_request_answer)

        self.login_window.update_user.connect(lambda: self.login_window.show_users(self.get_all_users()))
    def get_all_users(self):
        users = self.user_repo.get_all_users()
        return [{"id": u[0], "username": u[1], "avatar": u[2]} for u in users]

    def create_user(self, username, password, recovery_code):
        password_hash = self.password_hasher.hash(password) if password else None
        recovery_hash = self.password_hasher.hash(recovery_code)
        user_id = self.user_repo.create_user(username, password_hash, recovery_hash)
        self.user_session.set_user(self.user_repo.get_user_by_id(user_id)[0])
        self.user_created.emit(user_id)
        return user_id
    

    def change_username(self, new_name):
        self.user_repo.change_username_by_id(self.user_session.get_uid(), new_name)
        self.user_session.set_user(self.user_repo.get_user_by_id(self.user_session.get_uid())[0])

    def handle_password_change(self, password, new_password):
        user = self.user_repo.get_user_by_id(self.user_session.get_uid())[0]
        try:
            if user["password_hash"] is not None:
                self.password_hasher.verify(user['password_hash'], password)
            self.user_repo.change_password_by_id(user['user_id'], self.password_hasher.hash(new_password))
            user = self.user_repo.get_user_by_id(self.user_session.get_uid())[0]
            self.user_session.set_user(user)
            self.password_change_request_answer.emit(True)
        except (exceptions.VerifyMismatchError, exceptions.VerificationError):
            print("Неверный пароль!")
            self.password_change_request_answer.emit(False)

    def handle_password_recovery(self, user_id, code, new_password):
        user = self.user_repo.get_user_by_id(user_id)[0]
        try:
            self.password_hasher.verify(user["recovery_hash"] if user["recovery_hash"] is not None else '1', code )
            self.user_repo.change_password_by_id(
                user_id, self.password_hasher.hash(new_password)
            )
            user = self.user_repo.get_user_by_id(user_id)[0]
            self.user_session.set_user(user)
            self.password_recovery_request_answer.emit(True)
        except (exceptions.VerifyMismatchError, exceptions.VerificationError, exceptions.InvalidHashError):
            print("Неверный пароль!")
            self.password_recovery_request_answer.emit(False)

    def handle_login(self, user_id, password):
        """Обработчик входа (например, открывает MainWindow)."""
        user = self.user_repo.get_user_by_id(user_id)[0]
        try:
            if user["password_hash"] is not None:
                self.password_hasher.verify(user['password_hash'], password)
            self.user_session.set_user(user)
            print(f"Пользователь {self.user_session.get_user()} вошел в систему")
            self.successful_login.emit(user_id)
        except (exceptions.VerifyMismatchError, exceptions.VerificationError):
            print("Неверный пароль!")
            self.unsuccessful_login.emit(user_id)
        # Здесь можно передать управление в главный контроллер
