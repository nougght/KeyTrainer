from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QFileDialog, QMessageBox
from datetime import datetime, date, timedelta

# контроллер статистики
class StatisticsControl(QObject):
    show_statistics = Signal(list)

    def __init__(self, text_repository, user_repository, session_repository, time_points_repository, daily_activity_repository, main_window, user_session):
        super().__init__()
        self.sessions_page = 1

        self.main_window = main_window
        self.user_session = user_session
        self.text_repository = text_repository
        self.user_repository = user_repository
        self.session_repository = session_repository
        self.time_points_repository = time_points_repository
        self.daily_activity_repository = daily_activity_repository

        self.show_statistics.connect(main_window.typing_widget.on_show_statistics)

        self.main_window.statistics_widget.session_widget.to_page.connect(self.to_sessions_page)
        self.main_window.settings_widget.clear_user_data.connect(self.on_clear_data)
        self.main_window.settings_widget.export_user.connect(self.export_user)
        self.main_window.settings_widget.import_user.connect(self.import_user)
    
    # обработчик окончания тренировки
    # обновляет данные в бд и передает их в основное окно
    @Slot()
    def on_session_finished(self, session):
        user_id = self.user_session.get_uid()
        session = session.stats
        session_data = {
            key: value
            for key, value in session.items()
            if key not in ["time", "chars", "cpm", "wpm", "errors"]
        }

        # session_id = self.stats_repository.save_session(session_data)

        # time_points["session_id"] = session_id
        # self.stats_repository.save_time_points()

        session_id = self.session_repository.save_session(self.user_session.get_user()["user_id"], session_data)

        time_points = [
            (session_id, session["time"][i], session["chars"][i], session["cpm"][i], session["errors"][i])
            for i in range(len(session["time"]))
        ]

        self.time_points_repository.save_time_points(time_points)
        self.daily_activity_repository.update_activity(self.user_session.get_user()["user_id"], date.today(),
            (session["duration"], session["avg_cpm"], session["accuracy"]))
        self.user_repository.update_user_data(self.user_session.get_user()["user_id"], 
            (session["duration"], session["total_chars"], session["avg_cpm"]))

        session_stats = (self.session_repository.get_session(user_id, session_id), self.time_points_repository.get_session_points(session_id))

        self.show_statistics.emit(session_stats)
        self.show_general_stats(self.user_session.get_uid())

    # экспорт данных пользователя
    def export_user(self):
        user_id = self.user_session.get_uid()

        if user_id:
            user = self.user_repository.get_user_by_id(user_id)[0]
            sessions_id = self.session_repository.get_last_sessions(user_id, 0, 1000000)

            sessions = []
            points = []
            for id in sessions_id:
                sessions.append(self.session_repository.get_session(user_id, id[0]))
                points.append(self.time_points_repository.get_session_points(id[0]))

        file_path, _ = QFileDialog.getSaveFileName(
            self.main_window,
            caption="Сохранить SQL-дамп",
            dir=f"{user["username"]}",  # Начальная директория (пусто = текущая)
            filter="SQL Files (*.sql);;All Files (*)"  # Фильтры файлов
        )

        if file_path:  # Если пользователь не отменил выбор
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("BEGIN TRANSACTION;\n")
                q = f"INSERT OR REPLACE INTO users (user_id, username, password_hash, recovery_hash, avatar, sync_token) VALUES {user[0], user[1], user[2], user[3], user[4], 'temp'};\n"
                q = q.replace('None', 'Null')
                f.write(q)
                for i in range(len(sessions)):
                    session = sessions[i]
                    q = f"""INSERT OR REPLACE INTO sessions (user_id, session_id, start_time, test_type, duration_seconds, total_chars, avg_cpm, max_cpm, accuracy, total_errors, date) VALUES {
                    user_id,
                    sessions_id[i][0],
                    session["start_time"],
                    session["test_type"],
                    session["duration_seconds"],
                    session["total_chars"],
                    session["avg_cpm"],
                    session["max_cpm"],
                    session["accuracy"],
                    session["total_errors"],
                    session["start_time"].split(' ')[0]};\n"""
                    q = q.replace('None', 'Null')
                    f.write(q)

                for i in range(len(points)):
                    pointlist = points[i]
                    for point in pointlist:
                        f.write(
                            f"""INSERT OR REPLACE INTO time_points (point_id, session_id, second, chars, cpm, errors)
                        VALUES {
                            point[0],
                            sessions_id[i][0],
                            point[2],
                            point[3],
                            point[4],
                            point[5]
                        };\n"""
                        )
                f.write("COMMIT;\n")

    # импорт данных пользователя
    def import_user(self):
        import_file, _ = QFileDialog.getOpenFileName(
            self.main_window,
            "Выберите SQL-файл для импорта",
            "",  # Начальная директория
            "SQL Files (*.sql);;All Files (*)",  # Фильтры
        )

        if not import_file:  # Если пользователь отменил выбор
            return

        with open(import_file, "r", encoding="utf-8") as f:
            sql_script = f.read()

        with self.user_repository.db.get_connection() as db_connection:
            cursor = db_connection.cursor()
            cursor.executescript(sql_script)
            db_connection.commit()

        ret = QMessageBox.information(
            self.main_window,
            "KeyTrainer",
            self.tr("Аккаунт успешно импортирован!")
        )

        # self.main_window.settings_widget.user_leaved.emit()
    # удаления пользователя
    def delete_current_user(self, user_id=None):
        if user_id is None:
            user_id = self.user_session.get_uid()
        self.user_repository.delete_user_by_id(user_id)
        self.daily_activity_repository.delete_activity_by_id(user_id)

        session_ids = self.session_repository.get_last_sessions(user_id, 0, 1000000)
        for id in session_ids:
            self.session_repository.delete_session_by_id(id[0])
            self.time_points_repository.delete_points_by_id(id[0])
    # передача статистики в основное окно
    def show_general_stats(self, user_id):
        user_data = self.user_repository.get_user_data(user_id)
        activity = self.daily_activity_repository.get_activity_by_uid(user_id)
        mx = 0
        for act in activity:
            if act[3] > mx:
                mx = act[3]
            print('actttt', act[2])

        activity = {activity[i][2] : ((1 + round(activity[i][3] / mx * 3)), activity[i][3]) for i in range(len(activity)) if mx > 0}

        if user_data:
            td = timedelta(seconds=user_data["total_time"])

        self.main_window.statistics_widget.general_stats.update_ui(user_data)
        self.main_window.statistics_widget.activity_calendar.create_grid(activity, user_data['current_streak'], user_data['max_streak'], user_data['total_days'])

        # session_data = [session_data["start_time"], session_data["test_type"], session_data["duration_seconds"], session_data["total_chars"], session_data["avg_cpm"], session_data["max_cpm"], session_data["avg_cpm"]/5, f"{session_data["accuracy"]} / {session_data["total_errors"]}"]
        # chart_data = self.time_points_repository.get_session_points(24)

        sessions_id = self.session_repository.get_last_sessions(user_id, (self.sessions_page-1)*5, self.sessions_page*5)
        all_id = self.session_repository.get_last_sessions(user_id, 0, 1000)
        sessions_data = [(self.session_repository.get_session(user_id, id[0]), self.time_points_repository.get_session_points(id[0])) for id in sessions_id]
        self.main_window.statistics_widget.session_widget.load_page(((len(all_id) + 4) // 5), sessions_data)

        self.main_window.statistics_widget.distribution_chart.update_data([self.session_repository.get_session(user_id, id[0])['avg_cpm'] for id in all_id])

    def to_sessions_page(self, page):
        user_id = self.user_session.get_uid()
        self.sessions_page = page
        sessions_id = self.session_repository.get_last_sessions(user_id, (self.sessions_page-1)*5, self.sessions_page*5)
        all_id = self.session_repository.get_last_sessions(user_id, 0, 1000)
        sessions_data = [(self.session_repository.get_session(user_id, id[0]), self.time_points_repository.get_session_points(id[0])) for id in sessions_id]
        self.main_window.statistics_widget.session_widget.load_page(((len(all_id) + 4) // 5), sessions_data)

    def on_clear_data(self):
        user_id = self.user_session.get_uid()
        self.user_repository.clear_user_data(user_id)
        self.session_repository.clear_user_data(user_id)
        self.daily_activity_repository.clear_user_data(user_id)
        self.show_general_stats(user_id)
        self.to_sessions_page(1)
