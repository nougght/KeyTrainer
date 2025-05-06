from PySide6.QtCore import QObject, Signal, Slot
from datetime import datetime, date, timedelta

class StatisticsControl(QObject):
    show_statistics = Signal(list)

    def __init__(self, text_repository, user_repository, session_repository, time_points_repository, daily_activity_repository, main_window, user_session):
        super().__init__()
        self.main_window = main_window
        self.user_session = user_session
        self.text_repository = text_repository
        self.user_repository = user_repository
        self.session_repository = session_repository
        self.time_points_repository = time_points_repository
        self.daily_activity_repository = daily_activity_repository

        self.show_statistics.connect(main_window.typing_widget.on_show_statistics)
    @Slot()
    def on_session_finished(self, session):
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
        self.show_statistics.emit(self.time_points_repository.get_session_points(session_id))
        self.show_general_stats(self.user_session.get_uid())

    def show_general_stats(self, user_id):
        user_data = self.user_repository.get_user_data(user_id)
        activity = self.daily_activity_repository.get_activity_by_uid(user_id)
        mx = 0
        for act in activity:
            if act[3] > mx:
                mx = act[3]
            print('actttt', act[2])
        activity = {activity[i][2] : 1 + round(activity[i][3] / mx * 3) for i in range(len(activity))}
        td = timedelta(seconds=user_data["total_time"])


        self.main_window.statistics_widget.general_stats.update_ui(user_data)
        self.main_window.statistics_widget.activity_calendar.create_grid(activity, user_data['current_streak'], user_data['max_streak'], user_data['total_days'])
        
        sessions_id = self.session_repository.get_last_sessions(user_id, 0, 5)

        sessions_data = [(self.session_repository.get_session(user_id, id[0]), self.time_points_repository.get_session_points(id[0])) for id in sessions_id]
        # session_data = [session_data["start_time"], session_data["test_type"], session_data["duration_seconds"], session_data["total_chars"], session_data["avg_cpm"], session_data["max_cpm"], session_data["avg_cpm"]/5, f"{session_data["accuracy"]} / {session_data["total_errors"]}"]
        # chart_data = self.time_points_repository.get_session_points(24)
        self.main_window.statistics_widget.session_widget.load_page(1, sessions_data)


    def show_sessions_list(self):
        pass

    def expand_session(self):
        pass
    def collapse_session(self):
        pass
