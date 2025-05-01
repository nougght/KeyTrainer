# controllers/user_controller.py
from model import UserRepository


class UserController:
    def __init__(self, login_window, user_repo, user_session):
        self.user_session = user_session
        self.login_window = login_window
        self.user_repo = user_repo  # Зависимость от репозитория
        self.login_window.show_users(self.get_all_users())

        self.login_window.create_new_user.connect(self.create_user)
        self.login_window.user_selected.connect(self.handle_login)

    def get_all_users(self):
        """Возвращает список пользователей в удобном для View формате."""
        users = self.user_repo.get_all_users()
        return [{"id": u[0], "username": u[1], "avatar": u[2]} for u in users]

    def create_user(self, username):
        """Создает пользователя и возвращает его данные (или None, если ошибка)."""
        if not username:
            return None

        if self.user_repo.user_exists(username):
            return None  # или можно вызвать исключение

        user_id = self.user_repo.create_user(username)
        self.login_window.show_users(self.get_all_users())

    def handle_login(self, user_id):
        """Обработчик входа (например, открывает MainWindow)."""
        self.user_session.set_user(self.user_repo.get_user_by_id(user_id)[0])
        print(f"Пользователь {self.user_session.get_user()} вошел в систему")
        # Здесь можно передать управление в главный контроллер

