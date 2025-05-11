from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout, QScrollArea
)
from PySide6.QtCore import Signal, Slot, Qt, QMargins, QPropertyAnimation, Qt 
from PySide6.QtGui import QIcon, QAction, QPen, QColor, QPainter
from PySide6.QtCharts import QChart, QBarCategoryAxis, QLineSeries, QChartView, QValueAxis, QSplineSeries, QBarSeries, QBarSet


from PySide6.QtWidgets import QSizePolicy, QStackedWidget, QWidget, QGridLayout, QLabel, QVBoxLayout, QToolTip, QFrame, QHBoxLayout, QSizePolicy, QToolButton, QPushButton
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QColor, QPainter, QPen
import random

# виджет - основная статистика пользователя
class GeneralStatistics(QFrame):
    def __init__(self):
        super().__init__()
        self.grid_layout = QGridLayout(self)
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        self.grid_layout.setSpacing(10)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)

        self.l_titles = [self.tr("Дата регистрации:"), self.tr("Активных дней"), self.tr("Всего тренировок:")]
        self.r_up_titles = [self.tr("Общее время:"), self.tr("Набрано символов:"), self.tr("Лучший CPM:"), self.tr("Лучший WPM")]
        self.r_down_titles = [self.tr("Средний CPM:"),  self.tr("Средний WPM"), self.tr("Средняя точность:")]

        self.username = "username"
        self.l_values = ["2000 00 00", "45", "100"]
        self.r_up_values = ["1d 1h 1m", "3948", "300", "60"]
        self.r_down_values = ["250", "50", "80"]

        self.left_frame = QFrame()
        self.left_layout = QVBoxLayout(self.left_frame)
        self.left_layout.setSpacing(5)
        self.left_layout.setContentsMargins(25, 25, 25, 25)
        self.left_layout.addWidget(QLabel(self.username), 0, alignment=Qt.AlignmentFlag.AlignCenter)
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
        self.right_up_layout.setContentsMargins(25, 25, 25, 25)
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
        self.right_down_layout.setContentsMargins(25, 25, 25, 25)
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
        if data:
            self.l_values = [data[i] for i in range(1, 4)]
            self.r_up_values = [data[i] for i in range(4, 8)]
            self.r_up_values[2] = round(self.r_up_values[2], 2)
            self.r_up_values[3] = round(self.r_up_values[3], 2)
            self.r_down_values = [data[i] for i in range(8, 11)]
            self.r_down_values[0] = round(self.r_down_values[0], 2)
            self.r_down_values[1] = round(self.r_down_values[1], 2)
            self.r_down_values[2] = round(self.r_down_values[2]*100, 2)

            from datetime import timedelta
            print(data["total_time"])
            td = timedelta(seconds=data["total_time"])

            self.r_up_values[0] = str(td).split('.')[0] #time(second=int(user_data['total_time'])).isoformat()

            self.left_layout.itemAt(0).widget().setText(data[0])
            for i in range(len(self.l_values)):
                self.left_layout.itemAt(i + 1).layout().itemAt(1).widget().setText(str(self.l_values[i]))
            for i in range(len(self.r_up_values)):
                self.right_up_layout.itemAt(i).layout().itemAt(1).widget().setText(str(self.r_up_values[i]))
            for i in range(len(self.r_down_values)):
                self.right_down_layout.itemAt(i).layout().itemAt(1).widget().setText(str(self.r_down_values[i]))

# статистика одной тренировки
class SessionStatistics(QFrame):
    chart_hide = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        self.up_row_titles = [self.tr("Время старта"), self.tr("Тип тренировки"), self.tr("Длительность"), self.tr("Символов")]
        self.up_row_values = ["2000 01 01", "Текст/Русский", "100", "150"]
        self.down_row_titles = [self.tr("Средний CPM"), self.tr("Лучший CPM"), self.tr("Средний WPM"), self.tr("Точность/Ошибок")]
        self.down_row_values = ["250", "300", "50", "96% / 5"]

        self.frame_layout = QVBoxLayout(self)
        self.frame_layout.setContentsMargins(15, 15, 15, 15)
        self.up_row_widget = QFrame()
        self.up_row_layout = QHBoxLayout(self.up_row_widget)
        self.down_row_widget = QFrame()
        self.down_row_layout = QHBoxLayout(self.down_row_widget)
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

        self.frame_layout.addWidget(self.up_row_widget, 0, Qt.AlignmentFlag.AlignTop)
        self.frame_layout.addWidget(self.down_row_widget, 1, Qt.AlignmentFlag.AlignTop)

        self.is_chart_visible = False

        self.expand_button = QPushButton()
        self.expand_button.setText(self.tr('Показать график'))
        self.frame_layout.addWidget(self.expand_button, 2, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.expand_button.clicked.connect(lambda: self.set_chart_visible(not self.is_chart_visible))

        self.stack_chart = QStackedWidget()
        self.stack_chart.setContentsMargins(0, 0, 0, 0)
        self.stack_chart.layout().setContentsMargins(0, 0, 0, 0)
        self.stack_chart.setMaximumHeight(0)
        self.empty = QWidget()
        self.empty.setFixedHeight(0)
        self.chart = SessionChart()
        self.stack_chart.addWidget(self.empty)
        self.stack_chart.addWidget(self.chart)
        self.frame_layout.addWidget(self.stack_chart, 3, Qt.AlignmentFlag.AlignTop)
        # self.chart.hide()

    def set_chart_visible(self, is_visible):
        from PySide6.QtCore import QTimer
        if is_visible is True:
            self.expand_button.setText(self.tr('Скрыть график'))
            self.stack_chart.setCurrentIndex(1)
            self.stack_chart.setMaximumHeight(400)
            # self.chart.show()
        else:
            self.expand_button.setText(self.tr("Показать график"))
            self.stack_chart.setCurrentIndex(0)
            self.stack_chart.setMaximumHeight(0)
            # # self.setFixedHeight(self.height() - self.chart.height())
            # self.chart.hide()
            # self.adjustSize()
        # self.chart.setVisible(is_visible)
        self.is_chart_visible = is_visible

    def update_data(self, session_data, chart_data):
        for i in range(len(self.up_row_values)):
            self.up_row_values[i] = session_data[i]

        self.down_row_values[0] = round(session_data["avg_cpm"], 2)
        self.down_row_values[1] = round(session_data["max_cpm"], 2)
        self.down_row_values[2] = round(session_data["avg_cpm"] / 5, 2)
        self.down_row_values[3] = f"{round(session_data["accuracy"]*100, 2)}% / {session_data['total_errors']}"

        self.up_row_values[2] = round(self.up_row_values[2], 2)

        for i in range(len(self.up_row_values)):
            self.up_row_layout.itemAt(i).layout().itemAt(1).widget().setText(str(self.up_row_values[i]))
        for i in range(len(self.down_row_values)-1):
            self.down_row_layout.itemAt(i).layout().itemAt(1).widget().setText(str(self.down_row_values[i]))
        self.down_row_layout.itemAt(3).layout().itemAt(1).widget().setText(self.down_row_values[3])
        self.chart.update_data(chart_data)

    def event(self, event):
        from PySide6.QtCore import QEvent
        if event.type() == QEvent.Type.LanguageChange:
            self.retranslate()
        return super().event(event)

    def retranslate(self):
        self.up_row_titles = [self.tr("Время старта"), self.tr("Тип тренировки"), self.tr("Длительность"), self.tr("Символов")]
        self.down_row_titles = [self.tr("Средний CPM"), self.tr("Лучший CPM"), self.tr("Средний WPM"), self.tr("Точность/Ошибок")]

        for i in range(len(self.up_row_titles)):
            self.frame_layout.itemAt(0).widget().layout().itemAt(i).layout().itemAt(0).widget().setText(self.up_row_titles[i])
            self.frame_layout.itemAt(1).widget().layout().itemAt(i).layout().itemAt(0).widget().setText(self.down_row_titles[i])
        self.expand_button.setText(self.tr("Показать график"))

# список последних тренировок со статистикой
class ListWithPages(QFrame):
    to_page = Signal(int)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.page = 1
        self.page_items_number = 5
        self.total_pages = 1

        self.frame_layout = QVBoxLayout(self)

        self.list = QWidget()
        # self.list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        # self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.list_layout = QVBoxLayout(self.list)
        self.frame_layout.addWidget(self.list, 0)

        self.navigation = QHBoxLayout()
        self.prev_btn = QPushButton("<")
        self.next_btn = QPushButton(">")
        self.page_label = QLabel()
        self.update_label()

        self.prev_btn.clicked.connect(self.on_prev_btn)
        self.next_btn.clicked.connect(self.on_next_btn)

        self.navigation.addWidget(self.prev_btn)
        self.navigation.addWidget(self.page_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.navigation.addWidget(self.next_btn)
        self.frame_layout.addLayout(self.navigation, 1)

        for i in range(self.page_items_number):
            s = SessionStatistics()
            self.list_layout.addWidget(s)
            s.setVisible(False)

    def on_prev_btn(self):
        if self.page > 1:
            self.page -= 1
            self.to_page.emit(self.page)

    def on_next_btn(self):
        if self.page < self.total_pages:
            self.page += 1
            self.to_page.emit(self.page)

    def update_label(self):
        self.page_label.setText(f"{self.page} / {self.total_pages}")

    def load_page(self, total_pages, items_data):
        self.total_pages = total_pages
        for i in range(len(items_data)):
            self.list_layout.itemAt(i).widget().update_data(items_data[i][0], items_data[i][1])
            self.list_layout.itemAt(i).widget().setVisible(True)
        if not items_data:
            self.page = 0
            for i in range(self.page_items_number):
                self.list_layout.itemAt(i).widget().setVisible(False)
        self.update_label()

# календарь активности
class ActivityCalendar(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.tr("Календарь активности"))
        self.grid = None
        self.cs_label = None
        self.cs_text = None
        self.mx_text = None
        self.mx_label = None
        self.td_text = None
        self.td_label = None

    def create_grid(self, data, current_streak, max_streak, total_days):
        old_lo = self.layout()
        if old_lo:
            QWidget().setLayout(old_lo)
        self.setLayout(QVBoxLayout())
        labels = QHBoxLayout()

        self.cs_text = self.tr('Дней без перерыва')
        self.cs_label = QLabel(f'{self.cs_text}: {current_streak}')
        self.cs_label.setObjectName("streak")
        self.mx_text = self.tr("Максимум дней без перерыва")
        self.mx_label = QLabel(f"{self.mx_text}: {max_streak}")
        self.td_text = self.tr("Всего активных дней")
        self.td_label = QLabel(f'{self.td_text}: {total_days}')
        labels.addWidget(self.cs_label, alignment=Qt.AlignmentFlag.AlignBottom)
        labels.addWidget(self.mx_label, alignment=Qt.AlignmentFlag.AlignBottom)
        labels.addWidget(self.td_label, alignment=Qt.AlignmentFlag.AlignBottom)
        labels.addSpacing(4)

        self.layout().addLayout(labels, 0)

        self.grid = QGridLayout()
        self.grid.setSpacing(4)  # Аналог border-spacing в CSS!
        self.grid.setContentsMargins(5, 5, 5, 5)

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
                cell.setFixedSize(22, 22)  # Размер ячейки
                # cell.setAlignment(Qt.AlignCenter)

                # Получаем уровень активности (можно заменить на данные из SQLite)
                activity = data.get(date.toString("yyyy-MM-dd"))
                if activity is None:
                    activity = (0, 0)
                cell.setProperty("activity", f"{activity[0]}")
                cell.setObjectName("cell")
                self.tooltip_text = self.tr('Тренировок')
                tooltip = f"{date.toString('dd.MM.yyyy')}\n{self.tooltip_text}: {activity[1]}"
                cell.setToolTip(tooltip)

                # Устанавливаем цвет
                # cell.setStyleSheet(f"background-color: {color.name()}; border-radius: 2px;")

                # Добавляем tooltip с датой и активностью

                # Добавляем ячейку в сетку
                self.grid.addWidget(cell, day + 1, week, Qt.AlignmentFlag.AlignCenter)
                # Переходим к следующему дню
                date = date.addDays(1)

        # Добавляем сетку в основной layout
        self.layout().addLayout(self.grid, 1)

        for i in range(self.layout().count()):
            item = self.layout().itemAt(i)
            widget = item.layout()

            if widget:
                print(
                    f"  Cell [{i}] (span:): {widget.objectName() or widget.__class__.__name__}"
                )
            else:
                print(f"  Cell [{i}]: Empty or spacer")

        # Подпись месяцев (опционально)
        self.add_month_labels(self.grid)

    def add_month_labels(self, grid):
        self.months = [self.tr("Янв"),self.tr("Фев"),self.tr("Мар"),self.tr("Апр"),self.tr("Май"),self.tr("Июн"),self.tr("Июл"),self.tr("Авг"),self.tr("Сен"),self.tr("Окт"),self.tr("Ноя"),self.tr("Дек"),
        ]

        self.month_positions = [0,4,8,12,17,21,26,30,35,39,43,48,
        ]  # Примерные позиции

        for month, pos in zip(self.months, self.month_positions):
            label = QLabel(month)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # self.layout.addWidget(label)
            grid.addWidget(
                label, 9, pos, 1, 4, Qt.AlignmentFlag.AlignBottom
            )  # Размещаем над календарём

    def event(self, event):
        from PySide6.QtCore import QEvent
        if event.type() == QEvent.Type.LanguageChange:
            self.retranslate()
        return super().event(event)

    def retranslate(self):
        if self.grid is None:
            return
        self.setWindowTitle(self.tr("Календарь активности"))
        self.cs_text = self.tr("Дней без перерыва")
        self.mx_text = self.tr("Максимум дней без перерыва")
        self.td_text = self.tr("Всего активных дней")
        self.cs_label.setText(self.cs_text)
        self.mx_label.setText(self.mx_text)
        self.td_label.setText(self.td_text)

        current_year = QDate.currentDate().year()
        date = QDate(current_year, 1, 1)
        date.dayOfWeek()
        # Заполняем сетку
        for week in range(53):  # 53 недели в году (иногда)
            for day in range(7):  # 7 дней в неделе
                if date.year() > current_year:  # Если вышли за текущий год
                    continue
                if week == 0 and date.dayOfWeek() - 1 > day:
                    continue

                cell = self.grid.itemAtPosition(day+1, week).widget()
                self.tooltip_text = self.tr("Тренировок")
                tooltip = cell.toolTip()
                spl = tooltip.split('\n')
                spl[1] = self.tooltip_text + spl[1][spl[1].find(':'):]
                tooltip = '\n'.join(spl)

                cell.setToolTip(tooltip)

                date = date.addDays(1)
        self.months = [self.tr("Янв"),self.tr("Фев"),self.tr("Мар"),self.tr("Апр"),self.tr("Май"),self.tr("Июн"),self.tr("Июл"),self.tr("Авг"),self.tr("Сен"),self.tr("Окт"),self.tr("Ноя"),self.tr("Дек"),]
        for month, pos in zip(self.months, self.month_positions):
            self.grid.itemAtPosition(9, pos).widget().setText(month)

# график - распределение тренировок по скорости
class DistributionChart(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        # self.setAttribute(Qt.WA_TransparentForMouseEvents)
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)

    def setup_ui(self):
        from PySide6.QtGui import QFont
        from PySide6.QtCore import QMargins

        self.chart = QChart()
        self.chart.setMargins(QMargins(0, 0, 0, 0))
        font = QFont("Segoe UI", 15)
        # self.chart.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        self.setFixedHeight(400)
        self.chart.setMargins(QMargins(0, 0, 0, 0))
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        self.chart.setBackgroundBrush(QColor(40, 40, 40, 200))  # Тёмный фон
        self.chart.setBackgroundPen(Qt.PenStyle.NoPen)

        # self.chart.setTitleBrush(QColor("#FFFFFF"))       # Белый заголовок
        # self.chart.setTitleFont(QFont("Segoe UI", 14, QFont.Bold))
        self.chart.legend().setVisible(True)

        self.tests = QBarSeries()
        self.chart.addSeries(self.tests)

        axis_pen = QPen(QColor("#888888"))  # светло-серый с прозрачностью
        axis_pen.setWidth(1)
        label_color = QColor("#DDDDDD")

        self.axis_x = QBarCategoryAxis()
        self.axis_x.setTitleText("CPM")
        self.axis_y = QValueAxis()
        self.axis_y.setTitleText(self.tr("Тренировки"))
        self.chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignmentFlag.AlignLeft)
        for axis in self.chart.axes():
            axis.setTitleBrush(label_color)
            axis.setTitleFont(font)
            axis.setLabelsBrush(label_color)
            axis.setGridLinePen(axis_pen)
            axis.setLabelsFont(QFont("Segoe UI", 12))
            axis.setLinePen(axis_pen)

        self.tests.attachAxis(self.axis_x)
        self.tests.attachAxis(self.axis_y)

        self.chart.legend().setLabelColor(label_color)
        self.chart.legend().setFont(font)

        self.chart.setTitleBrush(label_color)
        self.chart.setTitleFont(self.chart.font())

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        # self.chart_view.setBackgroundBrush(QColor(40, 40, 40, 200))
        self.chart_view.setContentsMargins(0, 0, 0, 0)
        # self.chart_view.setStyleSheet("background: transparent; border: none;")

        # self.chart_view.setStyleSheet("""
        #     QChartView {
        #         border: 2px solid #00BFFF;
        #         border-radius: 12px;
        #         background-color: #1e1e1e;
        #     }
        # """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.chart_view)

        self.axis_x.setGridLineVisible(True)
        self.axis_y.setGridLineVisible(True)
        # self.axis_x.setLabelsVisible(False)

    def update_data(self, cpm_data):
        self.tests.clear()
        mx = int(max(cpm_data) // 50) + 1 if cpm_data else 0
        distribution = [0] * mx
        for cpm in cpm_data:
            r = int(cpm // 50)
            distribution[r] += 1

        self.bset = QBarSet(self.tr("Тренировки"))
        self.bset.append(distribution)
        self.bset.setColor(QColor("#379f3c"))
        self.bset.setBorderColor(QColor("#429721"))
        self.tests.setBarWidth(0.75)
        self.tests.append(self.bset)

        categories = [f"{i*50}-{(i+1)*50 - 1}" for i in range(mx+1)]
        self.axis_x.append(categories)

        self.axis_y.setRange(0, max(distribution if distribution else [0])+3)
        self.axis_y.setLabelFormat("%d")
        # self.axis_x.setRange(1, len(distribution))

# график скорости печати
class SessionChart(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        # self.setAttribute(Qt.WA_TransparentForMouseEvents)
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)

    def setup_ui(self):
        from PySide6.QtGui import QFont
        from PySide6.QtCore import QMargins
        self.chart = QChart()
        self.chart.setMargins(QMargins(0, 0, 0, 0))
        font = QFont("Segoe UI", 15)
        self.chart.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        self.setFixedHeight(400)
        self.chart.setMargins(QMargins(0, 0, 0, 0))
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        self.chart.setBackgroundBrush(QColor(40, 40, 40, 200))  # Тёмный фон
        self.chart.setBackgroundPen(Qt.PenStyle.NoPen)

        # self.chart.setTitleBrush(QColor("#FFFFFF"))       # Белый заголовок
        # self.chart.setTitleFont(QFont("Segoe UI", 14, QFont.Bold))
        self.chart.legend().setVisible(True)

        self.er = QBarSeries()
        self.chart.addSeries(self.er)

        axis_pen = QPen(QColor("#888888"))  # светло-серый с прозрачностью
        axis_pen.setWidth(1)
        label_color = QColor("#DDDDDD") 

        self.series = QSplineSeries()
        self.series.setPointsVisible(True)
        # self.chart.addSeries(self.series)
        self.prseries = QSplineSeries()
        self.prseries.setName(self.tr("Средний CPM"))
        self.prseries.setPointsVisible(True)
        self.chart.addSeries(self.prseries)
        self.smseries = QSplineSeries()
        self.smseries.setName(self.tr("Моментальный CPM"))
        self.smseries.setPointsVisible(True)
        self.chart.addSeries(self.smseries)

        self.axis_x = QValueAxis()
        self.axis_x.setTitleText(self.tr('Секунды'))
        self.axis_y = QValueAxis()
        self.axis_y.setTitleText(self.tr("CPM"))
        self.chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignmentFlag.AlignLeft)
        for axis in self.chart.axes():
            axis.setTitleBrush(label_color)
            axis.setTitleFont(font)
            axis.setLabelsBrush(label_color)
            axis.setGridLinePen(axis_pen)
            axis.setLabelsFont(QFont("Segoe UI", 12))
            axis.setLinePen(axis_pen)

        self.chart.legend().setLabelColor(label_color)
        self.chart.legend().setFont(font)
        # self.series.attachAxis(self.axis_x)
        # self.series.attachAxis(self.axis_y)
        self.prseries.attachAxis(self.axis_x)
        self.prseries.attachAxis(self.axis_y)
        self.smseries.attachAxis(self.axis_x)
        self.smseries.attachAxis(self.axis_y)
        self.er.attachAxis(self.axis_x)
        self.er.attachAxis(self.axis_y)

        self.chart.setTitleBrush(label_color)
        self.chart.setTitleFont(self.chart.font())

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        # self.chart_view.setBackgroundBrush(QColor(40, 40, 40, 200))
        self.chart_view.setContentsMargins(0, 0, 0, 0)
        # self.chart_view.setStyleSheet("background: transparent; border: none;")

        # self.chart_view.setStyleSheet("""
        #     QChartView {
        #         border: 2px solid #00BFFF;
        #         border-radius: 12px;
        #         background-color: #1e1e1e;
        #     }
        # """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.chart_view)

        # Стиль графика
        self.smseries.setPen(QPen(QColor("#00BFFF"), 2))

        self.prseries.setPen(QPen(QColor("#07E47D"), 3))

        self.axis_x.setGridLineVisible(True)
        self.axis_y.setGridLineVisible(True)
        # self.axis_x.setLabelsVisible(False)
        self.bset = None

    def update_data(self, cpm_data: list):
        self.prseries.clear()
        self.series.clear()
        self.smseries.clear()
        self.er.clear()
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
        self.bset_limit = max_cpm * 0.8
        ers = [float(c[5]) for c in cpm_data]
        max_er = max(ers)

        if max_er > 0:
            ers = [int(e / max_er * self.bset_limit) for e in ers]
        else:
            ers = [0 for _ in ers]
        ers.insert(0, 0)
        self.bset = QBarSet(self.tr("Ошибки"))
        self.bset.append(ers)
        self.bset.setColor(QColor("#FF5733"))
        self.er.remove(self.er.barSets()[0] if len(self.er.barSets()) else None)
        self.er.append(self.bset)

        self.axis_x.setRange(1, len(cpm))
        self.axis_x.setTickInterval(1)
        self.axis_x.setLabelFormat("%d")
        self.axis_y.setLabelFormat("%d")

    def show_overlay(self):
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

    def event(self, event):
        from PySide6.QtCore import QEvent
        if event.type() == QEvent.Type.LanguageChange:
            self.retranslate()
        return super().event(event)

    def retranslate(self):
        self.prseries.setName(self.tr("Средний CPM"))
        self.smseries.setName(self.tr("Моментальный CPM"))
        self.axis_x.setTitleText(self.tr("Секунды"))
        self.axis_y.setTitleText(self.tr("CPM"))
        if self.bset is not None:
            self.bset.setLabel(self.tr("Ошибки"))

# виджет(вкладка) статистики
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

        self.distribution_chart = DistributionChart()
        self.grid.addWidget(self.distribution_chart, 2, 0)
        self.session_widget = ListWithPages()
        self.grid.addWidget(self.session_widget, 3, 0)

    def event(self, event):
        from PySide6.QtCore import QEvent
        if event.type() == QEvent.Type.LanguageChange:
            self.retranslate()
        return super().event(event)

    def retranslate(self):
        self.distribution_chart.axis_y.setTitleText(self.tr("Тренировки"))
        self.distribution_chart.bset.setLabel(self.tr("Тренировки"))

        self.general_stats.l_titles = [self.tr("Дата регистрации:"), self.tr("Активных дней"), self.tr("Всего тренировок:")]
        self.general_stats.r_up_titles = [self.tr("Общее время:"), self.tr("Набрано символов:"), self.tr("Лучший CPM:"), self.tr("Лучший WPM")]
        self.general_stats.r_down_titles = [self.tr("Средний CPM:"),  self.tr("Средний WPM"), self.tr("Средняя точность:")]

        for i in range(len(self.general_stats.l_titles)):
            self.general_stats.layout().itemAtPosition(0, 0).widget().layout().itemAt(i + 1).layout().itemAt(0).widget().setText(self.general_stats.l_titles[i])
            self.general_stats.layout().itemAtPosition(0, 1).widget().layout().itemAt(i).layout().itemAt(0).widget().setText(self.general_stats.r_up_titles[i])
            self.general_stats.layout().itemAtPosition(1, 1).widget().layout().itemAt(i).layout().itemAt(0).widget().setText(self.general_stats.r_down_titles[i])
        self.general_stats.layout().itemAtPosition(0, 1).widget().layout().itemAt(i+1).layout().itemAt(0).widget().setText(self.general_stats.r_up_titles[i])
