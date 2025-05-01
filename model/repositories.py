class TextRepository:
    def __init__(self, db):
        self.db = db
    # источники:
    # oxford 3000 - https://github.com/jnoodle/English-Vocabulary-Word-List/tree/master
    # нкря (первые 6000) - https://ru.wiktionary.org/wiki/%D0%9F%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5:%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%87%D0%B0%D1%81%D1%82%D0%BE%D1%82%D0%BD%D0%BE%D1%81%D1%82%D0%B8_%D0%BF%D0%BE_%D0%9D%D0%9A%D0%A0%D0%AF:_%D0%A3%D1%81%D1%82%D0%BD%D0%B0%D1%8F_%D1%80%D0%B5%D1%87%D1%8C_1%E2%80%941000
    def get_random_words(self, language, quantity):
        with self.db.get_connection() as db_connection:
            cursor = db_connection.cursor()
            cursor.execute(
                """
                SELECT word FROM words
                WHERE language = ?
                ORDER BY RANDOM()
                LIMIT ?
                """,
                (language, quantity),
            )
            return [row["word"] for row in cursor.fetchall()]

    def get_words(self, language, length):
        words_list = self.get_random_words(language, length)
        return " ".join(words_list)

    def get_text(self, language, difficulty):
        with self.db.get_connection() as db_connection:
            cursor = db_connection.cursor()
            cursor.execute(
                """
                SELECT content FROM texts
                WHERE language = ? AND difficulty = ?
                ORDER BY RANDOM()
                LIMIT 1
                """,
                (language, difficulty),
            )
            return cursor.fetchall()[0]["content"]


class UserRepository:
    def __init__(self, db):
        self.db = db

    def get_user_by_id(self, user_id):
        with self.db.get_connection() as db_connection:
            cursor = db_connection.cursor()
            cursor.execute(
                """
                SELECT user_id, username, avatar FROM users
                WHERE user_id = ?
                """,
                (user_id,)
            )
            return cursor.fetchall()

    def get_all_users(self):
        """Возвращает список всех пользователей: (id, username, avatar)."""
        with self.db.get_connection() as db_connection:
            cursor = db_connection.cursor()
            cursor.execute(
                """
                SELECT user_id, username, avatar FROM users
                ORDER BY username
                """
            )
            return cursor.fetchall()

    def create_user(self, username, avatar=None):
        """Создает нового пользователя и возвращает его ID."""
        with self.db.get_connection() as db_connection:
            cursor = db_connection.cursor()
            cursor.execute(
                "INSERT INTO users (username, avatar, sync_token) VALUES (?, ?, ?)",
                (
                    username,
                    avatar,
                    "temp_token",
                ),  # В реальном приложении генерируйте токен
            )
            db_connection.commit()
            return cursor.lastrowid

    def user_exists(self, username: str) -> bool:
        """Проверяет, существует ли пользователь с таким именем."""
        with self.db.get_connection() as db_connection:
            cursor = db_connection.cursor()
            cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
            return cursor.fetchone() is not None

    def get_user_data(self, user_id):
        with self.db.get_connection() as db_connection:
            cursor = db_connection.cursor()
            cursor.execute(
                """
                SELECT username, avatar, created_at, sync_token, settings, total_time, total_sessions, total_chars, best_cpm, avg_cpm, avg_accuracy, max_streak, current_streak, total_days
                FROM users WHERE user_id = ?
                """
            )
            return cursor.fetchall()

    def calc_user_streak(self, user_id) -> tuple[int]:
        with self.db.get_connection() as db_connection:
            cursor = db_connection.cursor()
            # загрузка всех дней из сессий
            cursor.execute(
                """SELECT date FROM sessions
                    WHERE user_id = ?""",
                (user_id,),
            )
            from datetime import date, datetime

            # получение уникальных дней
            total_sessions = 0
            days = set()
            elem = cursor.fetchone()
            while elem != None:
                total_sessions += 1
                print(elem[0])
                days.add(elem[0])
                elem = cursor.fetchone()
            days = list(days)
            total_days = len(days)
            current_streak = 0
            max_streak = 0
            if total_days == 1:
                only_day = datetime.strptime(days[0], "%Y-%m-%d").date()
                current_streak = 1 if (only_day == date.today() or abs((only_day - date.today())).days == 1) else 0
                max_streak = current_streak if current_streak else 1
            elif total_days > 1:
                days.sort(reverse = True)
                # перевод из строки в datetime.date
                for i in range(len(days)):
                    days[i] = datetime.strptime(days[i], "%Y-%m-%d").date()
                print(days)
                td = date.today()
                current_streak = 0
                # вычисление текущего стрика
                i = -1
                if days[0] == td:
                    i = 0
                    while (i < len(days) - 1) and (days[i] - days[i + 1]).days == 1:
                        i += 1
                    current_streak = i + 1

                max_streak = current_streak
                st = 0
                for j in range(i + 1, len(days) - 1):
                    if (days[j] - days[j + 1]).days == 1:
                        st = (st + 1) if st != 0 else 2
                    elif st != 0:
                        if max_streak < st:
                            max_streak = st
                        st = 0
                if max_streak < st:
                    max_streak = st
        return {'total_sessions': total_sessions, 'current_streak': current_streak, 'max_streak': max_streak, 'total_days': total_days}

    def recalculate_user_data(self, user_id):
        new_data = None
        streak = self.calc_user_streak(user_id)
        with self.db.get_connection() as db_connection:
            cursor = db_connection.cursor()

            cursor.execute(
                """SELECT SUM(duration_seconds), SUM(total_chars), MAX(avg_cpm), AVG(avg_cpm), AVG(accuracy)
                    FROM sessions WHERE user_id = ?""",
                (user_id, ),
            )

            new_data = cursor.fetchone()
            if not new_data or new_data[0] is None:
                new_data = (0, 0, 0, 0, 0)
            cursor.execute(
                """UPDATE users SET
                total_sessions = ?,
                total_time = ?,
                total_chars = ?,
                best_cpm = ?,
                avg_cpm = ?,
                avg_accuracy = ?,
                max_streak = ?,
                current_streak = ?,
                total_days = ?
                WHERE user_id = ?""",
                (
                    streak['total_sessions'],
                    new_data[0],
                    new_data[1],
                    new_data[2],
                    new_data[3],
                    new_data[4],
                    streak['max_streak'],
                    streak['current_streak'],
                    streak['total_days'],
                    user_id
                ),
            )
        db_connection.commit()

    def update_user_data(self, user_id, new_data):
        with self.db.get_connection() as db_connection:
            cursor = db_connection.cursor()
            streak = self.calc_user_streak(user_id)
            print(streak['max_streak'], streak['current_streak'], streak['total_days'])

            cursor.execute(
                """UPDATE users SET
                    total_sessions = total_sessions + 1,
                    total_time = total_time + ?,
                    total_chars = total_chars + ?,
                    best_cpm = CASE WHEN ? > best_cpm THEN ? ELSE best_cpm END,
                    avg_cpm = (SELECT AVG(avg_cpm) FROM sessions WHERE user_id = ?),
                    avg_accuracy = (SELECT AVG(accuracy) FROM sessions WHERE user_id = ?),
                    max_streak = ?,
                    current_streak = ?,
                    total_days = ?
                    WHERE user_id = ?""",
                (
                    new_data[0],
                    new_data[1],
                    new_data[2],
                    new_data[2],
                    user_id,
                    user_id,
                    streak["max_streak"],
                    streak["current_streak"],
                    streak['total_days'],
                    user_id,
                ),
            )
            db_connection.commit()


import datetime as dt

class SessionRepository:
    def __init__(self, db):
        self.db = db

    # запрос в бд сессий пользователя, начиная со start по end, отсортированных от последних к старым
    def get_last_sessions(self, user_id, start, end):
        with self.db.get_connection() as db_connection:
            cursor = db_connection.cursor()
            cursor.execute(
                """
                SELECT * FROM sessions
                WHERE user_id = ?
                ORDER BY start_time DESC
                LIMIT ? OFFSET ?;
                """,
                (user_id, end - start, start),
            )
            return cursor.fetchall()

    def get_session(self, user_id, session_id):
        pass

    def save_session(self, user_id, session):
        with self.db.get_connection() as db_connection:
            cursor = db_connection.cursor()
            cursor.execute(
                """INSERT INTO sessions (user_id, start_time, duration_seconds, 
                total_chars, avg_cpm, max_cpm, accuracy, date, total_errors) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    user_id,
                    session["start_time"].strftime('%Y-%m-%d %H:%M:%S'),
                    session["duration"],
                    session["total_chars"],
                    session["avg_cpm"],
                    session["max_cpm"],
                    session["accuracy"],
                    dt.date.today(),
                    session["total_errors"]
                ),
            )
            db_connection.commit()
            return cursor.lastrowid

class TimePointsRepository:
    def __init__(self, db):
        self.db = db

    def save_time_points(self, time_points):
        query = """
        INSERT INTO time_points (session_id, second, chars, cpm, errors)
        VALUES (?, ?, ?, ?, ?)
        """

        # time_points = [
        #     (session["time"][i], session["chars"][i], session["cpm"][i], session["errors"][i]) for i in range(len(session["time"]))
        # ]

        with self.db.get_connection() as db_connection:
            cursor = db_connection.cursor()
            cursor.executemany(query, time_points)
            db_connection.commit()
            return cursor.lastrowid
    
    def get_session_points(self, session_id):
        with self.db.get_connection() as db_connection:
            cursor = db_connection.cursor()
            cursor.execute(
                """
                SELECT * FROM time_points
                WHERE session_id = ?
                ORDER BY second
                """,
                (session_id)
            )
            return cursor.fetchall()

class DailyActivityRepository:
    def  __init__(self, db):
        self.db = db

    def get_activity_by_uid_date(self, user_id, date):
        with self.db.get_connection() as db_connection:
            cursor = db_connection.cursor()
            cursor.execute(
                """SELECT * FROM daily_activity
                WHERE user_id = ? AND date = ?
                LIMIT 1 """,
                (user_id, date)
            )
            return cursor.fetchall()

    def save_activity(self, user_id, daily_activity):
        with self.db.get_connection() as db_connection:
            cursor = db_connection.cursor()
            cursor.execute(
                """INSERT INTO daily_activity (user_id, date, total_sessions, total_time, best_cpm, avg_cpm, avg_accuracy)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (user_id,) + daily_activity
            )
            return cursor.lastrowid

    def recalculate_activity(self, user_id, date):
        new_data = None
        exists = self.day_exists(user_id, date)
        with self.db.get_connection() as db_connection:
            cursor = db_connection.cursor()
            cursor.execute(
                """SELECT SUM(duration_seconds), MAX(avg_cpm), AVG(avg_cpm), AVG(accuracy)
                    FROM sessions WHERE user_id = ? AND date = ?""",
                (user_id, date),
            )
            new_data = cursor.fetchone()
            cursor.execute("""SELECT COUNT(*) FROM sessions WHERE user_id = ? AND date = ?""", (user_id, date))
            total_sessions = cursor.fetchone()[0]
            if self.day_exists(user_id, date):
                cursor.execute("""UPDATE daily_activity SET 
                    total_sessions = ?,
                    total_time = ?,
                    best_cpm = ?,
                    avg_cpm = ?,
                    avg_accuracy = ?
                    WHERE user_id = ? and date = ?""",
                    (total_sessions, new_data[0], new_data[1], new_data[2],new_data[3], user_id, date))
            else:
                self.save_activity(
                    user_id,
                    (
                        date,
                        len(new_data),
                        new_data[0],
                        new_data[1],
                        new_data[2],
                        new_data[3],
                    ),
                )

    def day_exists(self, user_id, date):
        with self.db.get_connection() as db_connection:
            cursor = db_connection.cursor()
            cursor.execute(
                """SELECT 1 FROM daily_activity WHERE user_id = ? AND date = ?""",
                (user_id, date),
            )
            return cursor.fetchone() is not None

    def update_activity(self, user_id, date, activity):
        exists = self.day_exists(user_id, date)
        new_time = activity[0]
        new_cpm = activity[1]
        if exists is True:
            with self.db.get_connection() as db_connection:
                cursor = db_connection.cursor()
                cursor.execute(
                    """UPDATE daily_activity SET 
                    total_sessions = total_sessions + 1,
                    total_time = total_time + ?,
                    avg_cpm = (SELECT AVG(avg_cpm) FROM sessions WHERE user_id = ? AND date = ?),
                    best_cpm = CASE WHEN ? > best_cpm THEN ? ELSE best_cpm END,
                    avg_accuracy = (SELECT AVG(accuracy) FROM sessions WHERE user_id = ? AND date = ?)
                    WHERE user_id = ? and date = ?""",
                    (new_time, user_id, date, new_cpm, new_cpm, user_id, date, user_id, date)
                )
        else:
            total_sessions = 1
            self.save_activity(user_id, (date, total_sessions, new_time, new_cpm, new_cpm, activity[-1]))
