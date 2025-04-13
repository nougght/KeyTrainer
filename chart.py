import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QPushButton, QSlider, QFrame)
from PySide6.QtCharts import (QChart, QChartView, QLineSeries, QBarSeries, 
                             QBarSet, QValueAxis, QBarCategoryAxis)
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

class BWChartDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анализ производительности (2020-2023)")
        self.resize(1000, 700)
        
        # Основной виджет со светлым фоном
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #ffffff;")
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Создаем график с светлой темой
        self.chart = QChart()
        self.chart.setTitle("Ключевые показатели эффективности")
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setBackgroundBrush(QBrush(Qt.white))
        
        # Стиль заголовка для Ч/Б печати
        title_font = QFont()
        title_font.setPixelSize(18)
        title_font.setBold(True)
        self.chart.setTitleFont(title_font)
        self.chart.setTitleBrush(QBrush(Qt.black))
        
        # Добавляем данные с Ч/Б-оптимизированными стилями
        self.create_bw_series()
        
        # Настройка осей для Ч/Б
        self.setup_bw_axes()
        
        # Создаем View для графика с рамкой
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setStyleSheet("border: 1px solid #cccccc;")
        
        # Панель управления в светлом стиле
        control_frame = QFrame()
        control_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f8f8;
                border: 1px solid #dddddd;
                padding: 8px;
            }
            QPushButton {
                background-color: #f0f0f0;
                color: #333333;
                border: 1px solid #cccccc;
                padding: 5px 12px;
                font-weight: normal;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QSlider::groove:horizontal {
                height: 6px;
                background: #e0e0e0;
            }
            QSlider::handle:horizontal {
                background: #808080;
                width: 16px;
                height: 16px;
                margin: -5px 0;
            }
        """)
        
        control_layout = QHBoxLayout(control_frame)
        control_layout.setSpacing(10)
        
        # Элементы управления
        self.zoom_in_btn = QPushButton("Увеличить")
        self.zoom_out_btn = QPushButton("Уменьшить")
        self.reset_btn = QPushButton("Сбросить")
        self.animation_slider = QSlider(Qt.Horizontal)
        self.animation_slider.setRange(0, 100)
        self.animation_slider.setValue(50)
        
        control_layout.addWidget(self.zoom_in_btn)
        control_layout.addWidget(self.zoom_out_btn)
        control_layout.addWidget(self.reset_btn)
        control_layout.addWidget(self.animation_slider)
        
        # Добавляем все в основной layout
        main_layout.addWidget(self.chart_view)
        main_layout.addWidget(control_frame)
        
        # Подключаем сигналы
        self.connect_signals()
        
        # Сохраняем график
        self.save_chart_image()

    def create_bw_series(self):
        """Создает серии данных, оптимизированные для Ч/Б"""
        years = ['2020', '2021', '2022', '2023']
        productivity = [65, 78, 82, 90]  # Производительность
        quality = [88, 92, 90, 95]       # Качество
        costs = [45, 38, 35, 32]          # Затраты
        
        # Основная линия (производительность) - толстая сплошная
        prod_series = QLineSeries()
        prod_series.setName("Производительность (%)")
        pen = QPen(Qt.black)
        pen.setWidth(3)
        pen.setStyle(Qt.SolidLine)
        prod_series.setPen(pen)
        
        for i, year in enumerate(years):
            prod_series.append(i, productivity[i])
        
        # Линия качества - пунктирная
        qual_series = QLineSeries()
        qual_series.setName("Качество (%)")
        pen = QPen(Qt.black)
        pen.setWidth(2)
        pen.setStyle(Qt.DashLine)
        qual_series.setPen(pen)
        
        for i, year in enumerate(years):
            qual_series.append(i, quality[i])
        
        # Столбцы затрат - различные узоры серого
        cost_series = QBarSeries()
        cost_set = QBarSet("Затраты (индекс)")
        
        patterns = [Qt.Dense4Pattern, Qt.Dense6Pattern, Qt.Dense7Pattern, Qt.BDiagPattern]
        for i, value in enumerate(costs):
            cost_set << value
        
        cost_series.append(cost_set)
        
        # Настройка стиля столбцов
        for bar in cost_series.barSets():
            bar.setBrush(QBrush(QColor("#808080"), patterns[0]))
            bar.setPen(QPen(Qt.black, 1))
        
        # Добавляем все серии на график
        self.chart.addSeries(prod_series)
        self.chart.addSeries(qual_series)
        self.chart.addSeries(cost_series)

    def setup_bw_axes(self):
        """Настраивает оси для Ч/Б печати"""
        # Ось X
        axis_x = QBarCategoryAxis()
        axis_x.append(['2020', '2021', '2022', '2023'])
        axis_x.setTitleText("Год")
        axis_x.setLabelsColor(Qt.black)
        axis_x.setTitleBrush(QBrush(Qt.black))
        axis_x.setGridLineColor(QColor("#cccccc"))
        self.chart.addAxis(axis_x, Qt.AlignBottom)
        
        # Основная ось Y
        axis_y = QValueAxis()
        axis_y.setTitleText("Показатель (%)")
        axis_y.setLabelFormat("%.0f")
        axis_y.setRange(0, 100)
        axis_y.setLabelsColor(Qt.black)
        axis_y.setTitleBrush(QBrush(Qt.black))
        axis_y.setGridLineColor(QColor("#dddddd"))
        axis_y.setLinePenColor(Qt.black)
        self.chart.addAxis(axis_y, Qt.AlignLeft)
        
        # Привязываем серии к осям
        for series in self.chart.series():
            series.attachAxis(axis_x)
            series.attachAxis(axis_y)
        
        # Стиль легенды для Ч/Б
        legend = self.chart.legend()
        legend.setLabelColor(Qt.black)
        legend.setAlignment(Qt.AlignBottom)
        legend.setBackgroundVisible(False)
        legend.setFont(QFont("Arial", 9))

    def connect_signals(self):
        """Подключает обработчики событий"""
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        self.zoom_out_btn.clicked.connect(self.zoom_out)
        self.reset_btn.clicked.connect(self.reset_view)
        self.animation_slider.valueChanged.connect(self.animate_chart)
        
        # Включение взаимодействия с графиком
        self.chart_view.setRubberBand(QChartView.RectangleRubberBand)
        self.chart_view.setDragMode(QChartView.ScrollHandDrag)

    def zoom_in(self):
        """Увеличивает масштаб графика"""
        self.chart.zoom(1.2)

    def zoom_out(self):
        """Уменьшает масштаб графика"""
        self.chart.zoom(0.8)

    def reset_view(self):
        """Сбрасывает вид графика к исходному"""
        self.chart.zoomReset()

    def animate_chart(self, value):
        """Анимация графика при движении слайдера"""
        factor = value / 50.0
        for series in self.chart.series():
            if isinstance(series, QLineSeries):
                for point in series.pointsVector():
                    new_y = point.y() * factor
                    series.replace(point, QPointF(point.x(), new_y))

    def save_chart_image(self):
        """Сохраняет график в файл с высоким качеством"""
        self.chart_view.grab().save("bw_chart.png", quality=100)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BWChartDemo()
    window.show()
    sys.exit(app.exec())