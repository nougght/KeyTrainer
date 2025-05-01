from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)
from PySide6.QtCore import Signal, Slot, Qt, QMargins, QPropertyAnimation
from PySide6.QtGui import QIcon, QAction, QPen, QColor, QPainter
from PySide6.QtCharts import QChart, QLineSeries, QChartView, QValueAxis

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


class chart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        # self.setAttribute(Qt.WA_TransparentForMouseEvents)
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)

    def setup_ui(self):
        self.chart = QChart()
        # self.chart.setBackgroundBrush(Qt.transparent)
        self.chart.setMargins(QMargins(0, 0, 0, 0))
        self.chart.legend().hide()

        self.series = QLineSeries()
        self.chart.addSeries(self.series)

        self.axis_x = QValueAxis()
        self.axis_y = QValueAxis()
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_x)
        self.series.attachAxis(self.axis_y)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setStyleSheet("background: transparent; border: none;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.chart_view)

        # Стиль графика
        pen = QPen(QColor(58, 110, 165))
        pen.setWidth(2)
        self.series.setPen(pen)
        self.axis_x.setGridLineVisible(False)
        self.axis_y.setGridLineVisible(False)
        self.axis_x.setLabelsVisible(False)

    def update_data(self, cpm_data: list):
        """Обновляет график новыми данными CPM"""
        self.series.clear()

        max_cpm = max(cpm_data) if cpm_data else 60
        self.axis_y.setRange(0, max_cpm * 1.2)  # +20% сверху

        for i, cpm in enumerate(cpm_data):
            self.series.append(i + 1, cpm)

        self.axis_x.setRange(0, len(cpm_data))

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


class StatisticsWidget(QWidget):
    key_theme_switch = Signal()
    difficulty_change = Signal(str)
    language_change = Signal(str)
    mod_change = Signal(str)

    def __init__(self):
        super().__init__()
