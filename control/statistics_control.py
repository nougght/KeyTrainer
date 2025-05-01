from PySide6.QtCore import QObject, Signal, Slot
from datetime import datetime, date

class StatisticsControl(QObject):
    show_statistics = Signal(list)

    def __init__(self, text_repository, user_repository, session_repository, time_points_repository, daily_activity_repository, main_window, user_session):
        super().__init__()
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
        self.show_statistics.emit(session["cpm"])
    
    def show_general_stats(self):
        pass

    def show_sessions_list(self):
        pass

    def expand_session(self):
        pass
    def collapse_session(self):
        pass

