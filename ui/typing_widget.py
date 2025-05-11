from PySide6.QtWidgets import (
    QFrame,
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QMenuBar,
    QPushButton,
    QSizePolicy,
    QProgressBar,
    QSpacerItem,
    QToolBar,
    QComboBox,
    QMessageBox,
    QToolButton,
    QStackedWidget
)
from PySide6.QtCore import Signal, Slot, Qt, QEvent
from PySide6.QtGui import QIcon, QAction

from ui.other_widgets import (
    KeyTextEdit,
    KeyProgressDisplay,
    KeyboardWidget,
    RadioList,
)
from ui.statistics_widget import SessionChart, SessionStatistics
from utils import resource_path

# виджет(вкладка) тренировки
class TypingWidget(QFrame):
    key_theme_switch = Signal()
    difficulty_change = Signal(str) # сигналы изменения параметров тренировки
    language_change = Signal(str)
    mod_change = Signal(str)

    def __init__(self):
        super().__init__()

        self.is_keyboard_visible = True
        # self.setWindowIcon(QIcon("resources/keyIc (2).ico"))

        # self.setCentralWidget(QWidget())
        self.setWindowTitle("Key Trainer")
        self.central_layout = QGridLayout(self)
        self.central_layout.setContentsMargins(30, 30, 30, 10)
        self.setStyleSheet('')

        # прогресс + ошибки при наборе
        self.char_pos_label = KeyProgressDisplay(1)
        self.central_layout.addWidget(
            self.char_pos_label, 2, 0, Qt.AlignmentFlag.AlignCenter
        )

        # прогресс бар в процентах
        self.progress_bar = QProgressBar(minimum=0, maximum=100)
        self.progress_bar.setTextVisible(False)
        self.central_layout.addWidget(
            self.progress_bar, 2, 1, Qt.AlignmentFlag.AlignVCenter
        )
        self.progress_bar.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding
        )
        # self.progress_bar.setTextVisible(False)

        # перключатель между полем с текстом и статистикой тренировки
        self.stack = QStackedWidget()

        self.train_display = QWidget()
        self.train_layout = QGridLayout(self.train_display) 

        self.text_display = KeyTextEdit() # кастомное текстовое поле
        self.text_display.setMinimumHeight(330)
        self.text_display.setMaximumHeight(500)
        self.text_display.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding
        )
        self.train_layout.addWidget(self.text_display, 0, 0, 1, 2, Qt.AlignmentFlag.AlignTop)
        # кастомный виджет клавиатуры
        self.keyboard_widget = KeyboardWidget("english")
        print(self.keyboard_widget.size().height(), self.keyboard_widget.size().width())
        self.key_theme_switch.connect(self.keyboard_widget.on_key_theme_switch)
        self.train_layout.addWidget(
            self.keyboard_widget, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.vert_spacer_3 = QSpacerItem(
            20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )
        self.train_layout.addItem(self.vert_spacer_3, 1, 0, 1, 2)
        # кастомный виджет вывода статистики
        self.session_stats = SessionStatistics()
        self.session_stats.expand_button.hide()
        self.session_stats.set_chart_visible(True)

        self.stack.addWidget(self.train_display)
        self.stack.addWidget(self.session_stats)

        self.stack.setCurrentIndex(0)
        self.central_layout.addWidget(self.stack, 3, 0, 1, 2)

        self.vert_spacer_1 = QSpacerItem(
            20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.vert_spacer_2 = QSpacerItem(
            20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )

        self.central_layout.addItem(self.vert_spacer_2, 1, 0, 1, 2)

        # self.central_layout.addItem(self.vert_spacer_3, 9, 0, 1, 2)
        # print(self.central_layout.rowCount())
        # print(self.central_layout.columnCount())
        # print(self.central_layout.itemAt(0))

        # self.theme_switch_button = QPushButton("Поменять тему")
        # self.theme_switch_button.setObjectName("themes")
        # # self.theme_switch_button.setIcon(QtGui.QIcon("data/themes.svg"))
        # self.central_layout.addWidget(
        #     self.theme_switch_button, 1, 0, Qt.AlignmentFlag.AlignLeft
        # )

        self.reset_button = QToolButton()
        # self.reset_button.setIcon(QIcon(resource_path('data/reset.png')))
        self.reset_button.setObjectName("reset")
        self.reset_button.clicked.connect(lambda: self.set_statistics_mode(False))
        # self.central_layout.addWidget(self.reset_button, 6, 1, Qt.AlignmentFlag.AlignRight)

        self.tool_layout = QToolBar()
        # self.tool_layout.setSpacing(0)
        # self.tool_layout.setContentsMargins(0, 0, 0, 0)
        self.tb_spacer1 = QWidget()

        self.tb_spacer1.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding,
            QSizePolicy.Policy.MinimumExpanding,
        )
        self.tool_layout.addWidget(self.tb_spacer1)

        self.lang_combo = QComboBox() # переключатель языка тренировки
        self.lang_combo.setObjectName("langComboBox")
        self.lang_combo.addItem(self.tr("Russian"), "russian")
        self.lang_combo.addItem(self.tr("English"), "english")
        self.lang_combo.addItem(self.tr("Python"), "python")
        self.lang_combo.addItem(self.tr("C++"), "cpp")
        self.lang_combo.currentIndexChanged.connect(
            lambda index: (self.language_change.emit(
                self.lang_combo.itemData(index)
            ), self.text_display.setFocus())
        )
        self.lang_combo.setCurrentIndex(1)
        self.tool_layout.addWidget(self.lang_combo)

        self.tb_spacer2 = QWidget()
        self.tb_spacer2.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding,
            QSizePolicy.Policy.MinimumExpanding,
        )
        self.tool_layout.addWidget(self.tb_spacer2)

        self.mode_list = RadioList() # переключение режима тренировки
        self.mode_list.setObjectName("modeList")
        self.mode_list.add_items([self.tr("Words"), self.tr("Text")])
        self.mode_list.button_group.button(0).clicked.connect(
            lambda: self.mod_change.emit("words")
        )
        self.mode_list.button_group.button(1).clicked.connect(
            lambda: self.mod_change.emit("text")
        )
        self.tool_layout.addWidget(self.mode_list)
        self.diff_list = RadioList()
        self.tb_spacer3 = QWidget()
        self.tb_spacer3.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding,
            QSizePolicy.Policy.MinimumExpanding,
        )
        self.tool_layout.addWidget(self.tb_spacer3)
        self.diff_list.setObjectName("diffList")  # переключение сложности тренировки
        self.diff_list.add_items([self.tr("Easy"), self.tr("Normal"), self.tr("Hard")])
        self.diff_list.button_group.button(0).clicked.connect(
            lambda: self.difficulty_change.emit("easy")
        )
        self.diff_list.button_group.button(1).clicked.connect(
            lambda: self.difficulty_change.emit("normal")
        )
        self.diff_list.button_group.button(2).clicked.connect(
            lambda: self.difficulty_change.emit("hard")
        )
        self.tool_layout.addWidget(self.diff_list)
        self.tool_layout.addWidget(self.reset_button)

        self.tb_spacer4 = QWidget()
        self.tb_spacer4.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding
        )
        self.tool_layout.addWidget(self.tb_spacer4)
        self.tb_spacer5 = QWidget()
        self.tb_spacer5.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding
        )
        # self.tool_layout.addWidget(self.tb_spacer5)

        self.central_layout.addWidget(self.tool_layout,0, 0, 1, 2)
        self.finish = QMessageBox()

        # for i in range(self.central_layout.count()):
        #     item = self.central_layout.itemAt(i)
        #     widget = item.widget()
        #     row, col, row_span, col_span = self.central_layout.getItemPosition(i)

        #     if widget:
        #         print(
        #             f"  Cell [{row}, {col}] (span: {row_span}x{col_span}): {widget.objectName() or widget.__class__.__name__}"
        #         )
        #     else:
        #         print(f"  Cell [{row}, {col}]: Empty or spacer")

    def set_keyboard_visible(self, is_visible):
        self.is_keyboard_visible = is_visible
        self.text_display.setMinimumHeight(300 if is_visible else 500)
        self.keyboard_widget.setVisible(is_visible)

    def setWindowStyle(self, style):
        self.text_display.document().setDefaultStyleSheet(style[1])
        self.text_display.setHtmlText()
        super().setStyleSheet(style[0])
        # print(styleSheet)
    # отображение статистики тренировки
    def set_statistics_mode(self, state: bool):
        if state:
            self.stack.setCurrentIndex(1)
        else:
            self.stack.setCurrentIndex(0)

    def on_show_statistics(self, data):
        self.session_stats.update_data(data[0], data[1])
        self.set_statistics_mode(True)

    @Slot()
    def on_stats_display(self, speed, typing_time):
        self.finish.setText(
            f"CPM - {speed:.2f} chars per minute\nTime - {typing_time:.2f} seconds"
        )
        # speed_lb = QLabel(f'CPM - {speed}', finish)
        self.finish.resize(500, 500)
        # self.finish.exec()

    @Slot()
    def on_exit_released(self):
        print("exit")
        self.close()

    # @Slot()
    # def on_rus_released(self):
    #     self.language_change.emit("russian")

    # @Slot()
    # def on_eng_released(self):
    #     self.language_change.emit("english")

    @Slot()
    def on_words_released(self):
        self.mod_change.emit("words")

    @Slot()
    def on_text_released(self):
        self.mod_change.emit("text")

    @Slot()
    def on_easy_released(self):
        self.difficulty_change.emit("easy")

    @Slot()
    def on_mid_released(self):
        self.difficulty_change.emit("normal")

    @Slot()
    def on_hard_released(self):
        self.difficulty_change.emit("hard")

    def on_key_theme_switch(self, style):
        self.key_theme_switch.emit()
        self.text_display.setFocus()

    def event(self, event):
        if event.type() == QEvent.Type.LanguageChange:
            self.retranslate()
        return super().event(event)
    # обновление надписей после смены языка
    def retranslate(self):
        self.lang_combo.setItemText(0, self.tr("Russian"))
        self.lang_combo.setItemText(1, self.tr("English"))
        self.lang_combo.setItemText(2, self.tr("Python"))
        self.lang_combo.setItemText(3, self.tr("C++"))

        self.mode_list.layout.itemAt(0).widget().setText(self.tr("Words"))
        self.mode_list.layout.itemAt(1).widget().setText(self.tr("Text"))

        self.diff_list.layout.itemAt(0).widget().setText(self.tr("Easy"))
        self.diff_list.layout.itemAt(1).widget().setText(self.tr("Normal"))
        self.diff_list.layout.itemAt(2).widget().setText(self.tr("Hard"))
        self.char_pos_label.er_mes = self.char_pos_label.tr("Ошибок")
        self.char_pos_label.setText(self.char_pos_label.get_text())