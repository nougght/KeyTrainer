from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout, QScrollArea
)
from PySide6.QtCore import Signal, Slot, Qt, QMargins, QPropertyAnimation, Qt 
from PySide6.QtGui import QIcon, QAction, QPen, QColor, QPainter
from PySide6.QtCharts import QChart, QLineSeries, QChartView, QValueAxis, QSplineSeries, QBarSeries, QBarSet


from PySide6.QtWidgets import QSizePolicy, QWidget, QGridLayout, QLabel, QVBoxLayout, QToolTip, QFrame, QHBoxLayout, QSizePolicy, QToolButton, QPushButton
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QColor, QPainter, QPen
import random

class GeneralStatistics(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Календарь активности")
        self.grid_layout = QGridLayout(self)
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        self.grid_layout.setSpacing(10)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)

        self.l_titles = ["Дата регистрации:", "Активных дней", "Всего тренировок:"]
        self.r_up_titles = ["Общее время:", "Набрано символов:", "Лучшее CPM:", "Лучшее WPM"]
        self.r_down_titles = ["Среднее CPM:",  "Среднее WPM", "Средняя точность:"]

        title = [
            "Дата регистрации:", "Всего тренировок:", "Активных дней", "Общее время:",
            "Набрано символов:", "Лучшее CPM:", "Среднее CPM:", "Лучшее WPM:", "Среднее WPM", "Средняя точность:"
        ]
        self.username = "username"
        self.l_values = ["2000 00 00", "45", "100"]
        self.r_up_values = ["1d 1h 1m", "3948", "300", "60"]
        self.r_down_values = ["250", "50", "80"]

        self.left_frame = QFrame()
        self.left_layout = QVBoxLayout(self.left_frame)
        self.left_layout.setSpacing(5)
        self.left_layout.addWidget(QLabel(self.username), 0)
        self.left_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.left_layout.itemAt(0).widget().setObjectName('uname_label')
        for i in range(len(self.l_titles)):
            lo = QVBoxLayout()
            lo.addWidget(QLabel(self.l_titles[i]), alignment=Qt.AlignmentFlag.AlignCenter)
            lo.itemAt(0).widget().setObjectName('title_label')
            lo.addWidget(QLabel(self.l_values[i]), alignment=Qt.AlignmentFlag.AlignCenter)
            lo.itemAt(1).widget().setObjectName("value_label")
            lo.setSpacing(0)
            self.left_layout.addLayout(lo, i + 1)

        self.right_up_frame = QFrame()
        self.right_up_layout = QHBoxLayout(self.right_up_frame)
        self.right_up_layout.setSpacing(100)
        self.right_up_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.right_up_layout.setContentsMargins(10, 20, 10, 20)
        for i in range(len(self.r_up_titles)):
            lo = QVBoxLayout()
            lo.addWidget(QLabel(self.r_up_titles[i]), alignment=Qt.AlignmentFlag.AlignCenter)
            lo.itemAt(0).widget().setObjectName("title_label")
            lo.addWidget(QLabel(self.r_up_values[i]), alignment=Qt.AlignmentFlag.AlignCenter)
            lo.itemAt(1).widget().setObjectName("value_label")
            lo.setSpacing(5)
            lo.setContentsMargins(1, 1, 1, 1)
            self.right_up_layout.addLayout(lo, i)

        self.right_down_frame = QFrame()
        self.right_down_layout = QHBoxLayout(self.right_down_frame)
        self.right_down_layout.setSpacing(200)
        self.right_down_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.right_down_layout.setContentsMargins(10, 20, 10, 20)
        for i in range(len(self.r_down_titles)):
            lo = QVBoxLayout()
            lo.addWidget(QLabel(self.r_down_titles[i]), alignment=Qt.AlignmentFlag.AlignCenter)
            lo.itemAt(0).widget().setObjectName("title_label")
            lo.addWidget(QLabel(self.r_down_values[i]), alignment=Qt.AlignmentFlag.AlignCenter)
            lo.itemAt(1).widget().setObjectName("value_label")
            self.right_down_layout.addLayout(lo, i)
            lo.setSpacing(5)

        self.grid_layout.addWidget(self.left_frame, 0, 0, 2, 1)
        self.grid_layout.addWidget(self.right_up_frame, 0, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.grid_layout.addWidget(self.right_down_frame, 1, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.created_date_label = QLabel('2000 00 00')
        self.sessions_label = QLabel('')

    def update_ui(self, data):
        self.l_values = [data[i] for i in range(1, 4)]
        self.r_up_values = [data[i] for i in range(4, 8)]
        self.r_up_values[2] = round(self.r_up_values[2], 2)
        self.r_up_values[3] = round(self.r_up_values[3], 2)
        self.r_down_values = [data[i] for i in range(8, 11)]
        self.r_down_values[0] = round(self.r_down_values[0], 2)
        self.r_down_values[1] = round(self.r_down_values[1], 2)
        self.r_down_values[2] = round(self.r_down_values[2]*100, 2)

        from datetime import timedelta

        td = timedelta(seconds=data["total_time"])
        self.r_up_values[0] = str(td) #time(second=int(user_data['total_time'])).isoformat()

        self.left_layout.itemAt(0).widget().setText(data[0])
        for i in range(len(self.l_values)):
            self.left_layout.itemAt(i + 1).layout().itemAt(1).widget().setText(str(self.l_values[i]))
        for i in range(len(self.r_up_values)):
            self.right_up_layout.itemAt(i).layout().itemAt(1).widget().setText(str(self.r_up_values[i]))
        for i in range(len(self.r_down_values)):
            self.right_down_layout.itemAt(i).layout().itemAt(1).widget().setText(str(self.r_down_values[i]))


class SessionStatistics(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        self.up_row_titles = ["Время старта", "Тип тренировки", "Длительность", "Символов"]
        self.up_row_values = ["2000 01 01", "Текст/Русский", "100", "150"]
        self.down_row_titles = ["Среднее CPM", "Лучшее CPM", "Среднее WPM", "Точность/Ошибок"]
        self.down_row_values = ["250", "300", "50", "96% / 5"]

        self.frame_layout = QVBoxLayout(self)
        self.up_row_layout = QHBoxLayout()
        self.down_row_layout = QHBoxLayout()
        for i in range(len(self.up_row_titles)):
            up_lo = QVBoxLayout()
            up_lo.addWidget(QLabel(self.up_row_titles[i]))
            up_lo.addWidget(QLabel(self.up_row_values[i]))
            up_lo.itemAt(0).widget().setObjectName("session_title_label")
            up_lo.itemAt(1).widget().setObjectName("session_value_label")
            self.up_row_layout.addLayout(up_lo)

            down_lo = QVBoxLayout()
            down_lo.addWidget(QLabel(self.down_row_titles[i]))
            down_lo.addWidget(QLabel(self.down_row_values[i]))
            down_lo.itemAt(0).widget().setObjectName("session_title_label")
            down_lo.itemAt(1).widget().setObjectName("session_value_label")
            self.down_row_layout.addLayout(down_lo)

        self.frame_layout.addLayout(self.up_row_layout, 0)
        self.frame_layout.addLayout(self.down_row_layout, 1)

        self.is_chart_visible = False

        self.expand_button = QPushButton()
        self.expand_button.setText('V Показать график')
        self.frame_layout.addWidget(self.expand_button, 2, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.expand_button.clicked.connect(lambda: self.set_chart_visible(not self.is_chart_visible))

        self.chart = SessionChart()
        self.frame_layout.addWidget(self.chart, 3)
        self.chart.hide()

        self.setStyleSheet(
            """
        SessionStatistics{
            border-radius: 10px;
            background: #f0f5ed;
            }
        
        SessionStatistics > QLabel#session_title_label {
            font-size: 15px;
            }
        SessionStatistics > QLabel#session_value_label {
            font-size: 35px;
            }
        """
        )

    def set_chart_visible(self, is_visible):
        if is_visible is True:
            self.expand_button.setText('^ Скрыть график')
            self.chart.show()
        else:
            self.expand_button.setText("V Показать график")
            # self.setFixedHeight(self.height() - self.chart.height())
            self.chart.hide()
            self.adjustSize()
        self.is_chart_visible = is_visible

    def update_data(self, session_data, chart_data):
        for i in range(len(self.up_row_values)):
            self.up_row_values[i] = session_data[i]
            self.down_row_values[i] = session_data[i + len(self.up_row_values)]

        self.up_row_values[2] = round(self.up_row_values[2], 2)
        self.down_row_values[0] = round(self.down_row_values[0], 2)
        self.down_row_values[2] = round(self.down_row_values[2], 2)

        for i in range(len(self.up_row_values)):
            self.up_row_layout.itemAt(i).layout().itemAt(1).widget().setText(str(self.up_row_values[i]))
        for i in range(len(self.down_row_values)-1):
            self.down_row_layout.itemAt(i).layout().itemAt(1).widget().setText(str(self.down_row_values[i]))
        self.down_row_layout.itemAt(3).layout().itemAt(1).widget().setText(f"{round(self.down_row_values[3], 2)}% / {session_data[-1]}")
        self.chart.update_data(chart_data)

class ListWithPages(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.page = 1
        self.page_items_number = 5
        self.total_pages = 1

        self.frame_layout = QVBoxLayout(self)

        self.list = QWidget()
        self.list_layout = QVBoxLayout(self.list)
        self.frame_layout.addWidget(self.list, 0)

        self.navigation = QHBoxLayout()
        self.prev_btn = QPushButton("<")
        self.next_btn = QPushButton(">")
        self.page_label = QLabel(f"1 из {self.total_pages}")

        self.navigation.addWidget(self.prev_btn)
        self.navigation.addWidget(self.page_label)
        self.navigation.addWidget(self.next_btn)
        self.frame_layout.addLayout(self.navigation, 1)

        for i in range(self.page_items_number):
            self.list_layout.addWidget(SessionStatistics())

    def load_page(self, number, items_data):
        for i in range(self.page_items_number):
            self.list_layout.itemAt(i).widget().update_data(items_data[i][0], items_data[i][1])

class ActivityCalendar(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Календарь активности")
        # self.setFixedSize(800, 200)  # Фиксированный размер (можно менять)

        # Основной layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Создаем сетку для календаря
        # with open("styles/defaultLight/widgetStyle.qss") as f:
        #     self.setStyleSheet(f.read())

    def create_grid(self, data, current_streak, max_streak, total_days):
        labels = QHBoxLayout()

        cs_label = QLabel(f'Дней без перерыва: {current_streak}')
        mx_label = QLabel(f'Максимум дней без перерыва: {max_streak}')
        td_label = QLabel(f'Всего активных дней: {total_days}')
        labels.addWidget(cs_label, alignment=Qt.AlignmentFlag.AlignBottom)
        labels.addWidget(mx_label, alignment=Qt.AlignmentFlag.AlignBottom)
        labels.addWidget(td_label, alignment=Qt.AlignmentFlag.AlignBottom)
        labels.addSpacing(4)

        self.layout.addLayout(labels, 0)

        """Создает сетку календаря (53 недели x 7 дней)."""
        grid = QGridLayout()
        grid.setSpacing(4)  # Аналог border-spacing в CSS!
        grid.setContentsMargins(5, 5, 5, 5)

        # Настройка цветов активности (как на GitHub)
        self.colors = [
            QColor(235, 237, 240),  # 0 активность
            QColor(155, 233, 168),  # 1
            QColor(64, 196, 99),  # 2
            QColor(48, 161, 78),  # 3
            QColor(33, 110, 57),  # 4 (максимум)
        ]

        # Текущий год и начальная дата (1 января)
        current_year = QDate.currentDate().year()
        date = QDate(current_year, 1, 1)
        date.dayOfWeek()
        # Заполняем сетку
        for week in range(53):  # 53 недели в году (иногда)
            for day in range(7):  # 7 дней в неделе
                if date.year() > current_year:  # Если вышли за текущий год
                    continue
                if week == 0 and date.dayOfWeek()-1>day:
                    continue
                wd = date.dayOfWeek()
                # Создаем ячейку
                cell = QFrame()
                
                cell.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                cell.setFixedSize(20, 20)  # Размер ячейки
                # cell.setAlignment(Qt.AlignCenter)

                # Получаем уровень активности (можно заменить на данные из SQLite)
                activity = data.get(date.toString("yyyy-MM-dd"))
                if activity is None:
                    activity = 0
                cell.setProperty("activity", f"{activity}")
                cell.setObjectName("cell")
                color = self.colors[activity]
                tooltip_text = f"{date.toString('dd.MM.yyyy')}\nАктивность: {activity}"
                cell.setToolTip(tooltip_text)

                # Устанавливаем цвет
                # cell.setStyleSheet(f"background-color: {color.name()}; border-radius: 2px;")

                # Добавляем tooltip с датой и активностью

                # Добавляем ячейку в сетку
                grid.addWidget(cell, day + 1, week, Qt.AlignmentFlag.AlignCenter)

                # Переходим к следующему дню
                date = date.addDays(1)

        # Добавляем сетку в основной layout
        self.layout.addLayout(grid, 1)

        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            widget = item.layout()
            
            if widget:
                print(
                    f"  Cell [{i}] (span:): {widget.objectName() or widget.__class__.__name__}"
                )
            else:
                print(f"  Cell [{i}]: Empty or spacer")

        # Подпись месяцев (опционально)
        self.add_month_labels(grid)

    def add_month_labels(self, grid):
        """Добавляет подписи месяцев над календарём."""
        months = ["Янв","Фев","Мар","Апр","Май","Июн","Июл","Авг","Сен","Окт","Ноя","Дек",
        ]

        month_positions = [0,4,8,12,17,21,26,30,35,39,43,48,
        ]  # Примерные позиции

        for month, pos in zip(months, month_positions):
            label = QLabel(month)
            label.setAlignment(Qt.AlignCenter)
            # self.layout.addWidget(label)
            grid.addWidget(
                label, 9, pos, 1, 4, Qt.AlignmentFlag.AlignBottom
            )  # Размещаем над календарём


# from ui.other_widgets import (
#     KeyWidget,
#     KeyTextEdit,
#     KeyProgressDisplay,
#     KeyboardWidget,
#     RadioList,
# )

# class chart(QChart):
#     def __init__(self, cpm, parent=None):
#         super().__init__(parent=parent)
#         self.setTitle('График')
#         prod_series = QLineSeries()
#         prod_series.setName("Производительность (%)")
#         pen = QPen(Qt.black)
#         pen.setWidth(3)
#         pen.setStyle(Qt.SolidLine)
#         prod_series.setPen(pen)

#         for i in range(len(cpm)):
#             prod_series.append(i, cpm[i])


class SessionChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        # self.setAttribute(Qt.WA_TransparentForMouseEvents)
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)

    def setup_ui(self):
        self.chart = QChart()
        self.setFixedHeight(400)
        # self.chart.setBackgroundBrush(Qt.transparent)
        self.chart.setMargins(QMargins(0, 0, 0, 0))
        self.chart.legend().hide()
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        self.chart.setBackgroundBrush(QColor("#121212"))  # Тёмный фон
        self.chart.setTitleBrush(QColor("#FFFFFF"))       # Белый заголовок
        # self.chart.setTitleFont(QFont("Segoe UI", 14, QFont.Bold))
        self.chart.legend().setVisible(False)

        self.er = QBarSeries()
        self.chart.addSeries(self.er)

        self.series = QSplineSeries()
        self.series.setPointsVisible(True)
        # self.chart.addSeries(self.series)
        self.prseries = QSplineSeries()
        self.prseries.setPointsVisible(True)
        self.chart.addSeries(self.prseries)
        self.smseries = QSplineSeries()
        self.smseries.setPointsVisible(True)
        self.chart.addSeries(self.smseries)

        self.axis_x = QValueAxis()
        self.axis_y = QValueAxis()
        self.chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignmentFlag.AlignLeft)
        for axis in self.chart.axes():
            axis.setLabelsBrush(QColor("#BBBBBB"))
            axis.setGridLineColor(QColor("#444444"))
            axis.setLinePen(QPen(QColor("#888888")))
            axis.setTitleText("")

        # self.series.attachAxis(self.axis_x)
        # self.series.attachAxis(self.axis_y)
        self.prseries.attachAxis(self.axis_x)
        self.prseries.attachAxis(self.axis_y)
        self.smseries.attachAxis(self.axis_x)
        self.smseries.attachAxis(self.axis_y)
        self.er.attachAxis(self.axis_x)
        self.er.attachAxis(self.axis_y)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.chart_view.setStyleSheet("background: transparent; border: none;")

        self.chart_view.setStyleSheet("""
            QChartView {
                border: 2px solid #00BFFF;
                border-radius: 12px;
                background-color: #1e1e1e;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.chart_view)

        # Стиль графика
        pen = QPen(QColor("#00BFFF"))
        pen.setWidth(1)
        self.smseries.setPen(pen)

        pen = QPen(QColor("#07e47d"))
        pen.setWidth(3)
        self.prseries.setPen(pen)

        self.axis_x.setGridLineVisible(False)
        self.axis_y.setGridLineVisible(False)
        # self.axis_x.setLabelsVisible(False)

    def update_data(self, cpm_data: list):
        """Обновляет график новыми данными CPM"""
        self.series.clear()
        cpm = [elem[4] for elem in cpm_data]
        prs = [cpm_data[0][3]]
        for i in range(1, len(cpm_data)):
            prs.append(cpm_data[i][3] + prs[i-1])

        window = 3
        smoothed = [(cpm_data[0][3]+cpm_data[1][3])*30]
        for i in range(1, len(cpm_data)):
            start = max(0, i - window + 1)
            avg = sum(c[3] for c in cpm_data[start:i+1]) / (i - start + 1)
            smoothed.append(avg * 60)

        max_cpm = max(cpm) if cpm else 60
        self.axis_y.setRange(0, max_cpm * 1.2)  # +20% сверху

        for i, c in enumerate(cpm):
            self.series.append(i + 1, c)

        for i, c in enumerate(prs):
            self.prseries.append(i + 1, (c / (i + 1)) * 60)

        for i, c in enumerate(smoothed):
            self.smseries.append(i + 1, c)
        bset = QBarSet('Ошибки')
        ers = []
        for c in cpm_data:
            ers.append(c[5])
        max_er = max(ers)
        if max_er:
            for i in range(len(ers)):
                ers[i] = ers[i] / max_er * max_cpm
        bset.append(ers)
        bset.setColor("#aa0c0c")
        self.er.append(bset)

        self.axis_x.setRange(1, len(cpm))

    def show_overlay(self):
        """Показывает оверлей с анимацией"""
        parent_window = self.parent()
        width = int(parent_window.width() * 0.3)
        height = int(parent_window.height() * 0.2)
        self.resize(width, height)

        # Позиционируем в правом верхнем углу с отступом 20px
        x = parent_window.x() + parent_window.width() - width - 20
        y = parent_window.y() + 20
        self.move(x, y)

        self.setWindowOpacity(0)
        self.show()
        # Анимация появления
        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setDuration(300)
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(0.9)
        self.fade_in_animation.start()


class TimePointsRepository:
    def __init__(self, db = None):
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

    def get_session_points(self, session_id, connection):
        with self.db.get_connection() if self.db else connection as db_connection:
            cursor = db_connection.cursor()
            cursor.execute(
                """
                SELECT * FROM time_points
                WHERE session_id = ?
                ORDER BY second
                """,
                (session_id, )
            )
            return cursor.fetchall()

chart_style = """"""

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sqlite3
    app = QApplication()
    window = SessionChart()
    # window.chart_view.setStyleSheet(chart_style)
    conn = sqlite3.connect("C:\PythonProjects\pyKey\data\data.db")
    repo = TimePointsRepository()
    points = repo.get_session_points(27, conn)
    window.update_data(points)
    window.show()
    ac = ActivityCalendar()
    ac.create_grid({}, 5, 18, 45)
    ac.show()

    # session_repo = Session
    session = SessionStatistics()
    session.show()
    app.exec()


class StatisticsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout(self)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        self.scroll_widget = QWidget()
        self.grid = QGridLayout(self.scroll_widget)

        self.main_layout.addWidget(self.scroll_area)
        self.scroll_area.setWidget(self.scroll_widget)
        self.grid.setSpacing(5)
        self.activity_calendar = ActivityCalendar()
        self.activity_calendar.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.general_stats = GeneralStatistics()
        self.grid.addWidget(self.general_stats, 0, 0, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(self.activity_calendar, 1, 0, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self.session_widget = ListWithPages()
        self.grid.addWidget(self.session_widget, 2, 0)
