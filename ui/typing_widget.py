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
)
from PySide6.QtCore import Signal, Slot, Qt
from PySide6.QtGui import QIcon, QAction

from ui.other_widgets import (
    KeyTextEdit,
    KeyProgressDisplay,
    KeyboardWidget,
    RadioList,
)
from ui.statistics_widget import SessionChart

class TypingWidget(QFrame):
    key_theme_switch = Signal()
    difficulty_change = Signal(str)
    language_change = Signal(str)
    mod_change = Signal(str)

    def __init__(self):
        super().__init__()

        self.setStyleSheet("width: 100%")
        self.setWindowIcon(QIcon("resources/keyIc (2).ico"))

        # self.setCentralWidget(QWidget())
        self.setWindowTitle("Key Trainer")
        self.central_layout = QGridLayout(self)
        self.setStyleSheet('')

        # панель меню
        self.mBar = QMenuBar()
        # self.mBar.setNativeMenuBar(True)
        self.mBar.addAction("Профиль")
        self.mBar.addAction("Настройки")
        self.mBar.addAction("Статистика")

        self.right_widget = QWidget()
        self.right_widget.setObjectName("Corner")
        layout = QHBoxLayout(self.right_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.minimise_btn = QPushButton("—")
        self.minimise_btn.setObjectName("minimiseButton")
        self.minimise_btn.pressed.connect(self.showMinimized)
        self.close_btn = QPushButton("✕")
        self.close_btn.setObjectName("exitButton")
        self.close_btn.pressed.connect(self.on_exit_released)
        layout.addWidget(self.minimise_btn)
        layout.addWidget(self.close_btn)

        # Добавляем виджет в правый угол меню-бара
        self.mBar.setCornerWidget(self.right_widget)

        self.mb_spacer1 = QWidget()
        self.mb_spacer1.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding,
            QSizePolicy.Policy.MinimumExpanding,
        )
        # self.setMenuBar(self.mBar)

        # lang_group = QtWidgets.QButtonGroup()
        # ru_btn = QtWidgets.QRadioButton()
        # ru_btn.setText('yo')
        # en_btn = QtWidgets.QRadioButton()
        # en_btn.setText('oy')

        # lang_group.addButton(ru_btn, id=0)
        # lang_group.addButton(en_btn, id=1)
        # self.central_layout.addWidget(ru_btn)
        # self.central_layout.addWidget(en_btn)

        # прогресс + ошибки при наборе
        self.char_pos_label = KeyProgressDisplay(1)
        self.central_layout.addWidget(
            self.char_pos_label, 1, 0, Qt.AlignmentFlag.AlignCenter
        )

        # прогресс бар в процентах
        self.progress_bar = QProgressBar(minimum=0, maximum=100)
        self.progress_bar.setTextVisible(False)
        self.central_layout.addWidget(
            self.progress_bar, 1, 1, Qt.AlignmentFlag.AlignVCenter
        )
        self.progress_bar.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding
        )
        # self.progress_bar.setTextVisible(False)

        # поле текста
        self.text_display = KeyTextEdit()
        self.text_display.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding
        )
        self.central_layout.addWidget(self.text_display, 2, 0, 1, 2)

        self.chart = SessionChart()
        self.central_layout.addWidget(self.chart, 2, 0, 1, 2)
        self.chart.hide()

        self.vert_spacer_1 = QSpacerItem(
            20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.vert_spacer_2 = QSpacerItem(
            20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )
        self.vert_spacer_3 = QSpacerItem(
            20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )

        self.central_layout.addItem(self.vert_spacer_2, 0, 0, 1, 2)
        self.central_layout.addItem(self.vert_spacer_3, 3, 0, 1, 2)

        # self.central_layout.addItem(self.vert_spacer_3, 9, 0, 1, 2)
        print(self.central_layout.rowCount())
        print(self.central_layout.columnCount())
        print(self.central_layout.itemAt(0))

        self.keyboard_widget = KeyboardWidget("english")
        print(self.keyboard_widget.size().height(), self.keyboard_widget.size().width())
        self.key_theme_switch.connect(self.keyboard_widget.on_key_theme_switch)
        self.central_layout.addWidget(
            self.keyboard_widget, 4, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.theme_switch_button = QPushButton("Поменять тему")
        self.theme_switch_button.setObjectName("themes")
        # # self.theme_switch_button.setIcon(QtGui.QIcon("data/themes.svg"))
        # self.central_layout.addWidget(
        #     self.theme_switch_button, 1, 0, Qt.AlignmentFlag.AlignLeft
        # )

        self.reset_button = QPushButton("⟳")
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

        self.lang_combo = QComboBox()
        self.lang_combo.setObjectName("langComboBox")
        self.lang_combo.addItem("Russian")
        self.lang_combo.addItem("English")
        self.lang_combo.currentIndexChanged.connect(
            lambda index: self.language_change.emit(
                self.lang_combo.itemText(index).lower()
            )
        )
        self.tool_layout.addWidget(self.lang_combo)

        # self.rus_action = QtWidgets.QWidgetAction(self.tool_layout)
        # self.rus_action.setText("Russian")
        # self.tool_layout.addAction(self.rus_action)
        # self.rus_action.triggered.connect(self.on_rus_released)

        # self.eng_action = QtWidgets.QWidgetAction(self.tool_layout)
        # self.eng_action.setText("English")
        # self.tool_layout.addAction(self.eng_action)
        # self.eng_action.triggered.connect(self.on_eng_released)

        self.tb_spacer2 = QWidget()
        self.tb_spacer2.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding,
            QSizePolicy.Policy.MinimumExpanding,
        )
        self.tool_layout.addWidget(self.tb_spacer2)

        # self.words_action = QtWidgets.QWidgetAction(self.tool_layout)
        # self.words_action.setText("Words")
        # self.tool_layout.addAction(self.words_action)
        # self.words_action.triggered.connect(self.on_words_released)

        # self.text_action = QtWidgets.QWidgetAction(self.tool_layout)
        # self.text_action.setText("Text")
        # self.tool_layout.addAction(self.text_action)
        # self.text_action.triggered.connect(self.on_text_released)

        self.mode_list = RadioList()
        self.mode_list.setObjectName("modeList")
        self.mode_list.add_items(["Words", "Text"])
        self.mode_list.button_group.button(0).clicked.connect(
            lambda: self.mod_change.emit("words")
        )
        self.mode_list.button_group.button(1).clicked.connect(
            lambda: self.mod_change.emit("text")
        )
        self.tool_layout.addWidget(self.mode_list)
        diff_list = RadioList()
        self.tb_spacer3 = QWidget()
        self.tb_spacer3.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding,
            QSizePolicy.Policy.MinimumExpanding,
        )
        self.tool_layout.addWidget(self.tb_spacer3)
        diff_list.setObjectName("diffList")
        diff_list.add_items(["Easy", "Normal", "Hard"])
        diff_list.button_group.button(0).clicked.connect(
            lambda: self.difficulty_change.emit("easy")
        )
        diff_list.button_group.button(1).clicked.connect(
            lambda: self.difficulty_change.emit("normal")
        )
        diff_list.button_group.button(2).clicked.connect(
            lambda: self.difficulty_change.emit("hard")
        )
        self.tool_layout.addWidget(diff_list)

        self.tool_layout.addWidget(self.reset_button)
        # list_widget = QtWidgets.QListWidget()
        # list_widget.setFlow(list_widget.Flow.LeftToRight)
        # list_widget.setWrapping(True)
        # list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # list_widget.setSizeAdjustPolicy(QtWidgets.QListWidget.SizeAdjustPolicy.AdjustToContents)
        # list_widget.addItems(["Easy", "Normal", "Hard"])
        # list_widget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        # list_widget.adjustSize()
        # list_widget.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        # list_widget.setSizePolicy(
        #     QtWidgets.QSizePolicy.Policy.Fixed,
        #     QtWidgets.QSizePolicy.Policy.Fixed,
        # )

        # self.action1 = QtWidgets.QWidgetAction(self.tool_layout)
        # self.action1.setText("Easy")
        # self.tool_layout.addAction(self.action1)
        # self.action1.triggered.connect(self.on_easy_released)

        # self.action2 = QtWidgets.QWidgetAction(self.tool_layout)
        # self.action2.setText("Normal")
        # self.tool_layout.addAction(self.action2)
        # self.action2.triggered.connect(self.on_mid_released)

        # self.action3 = QtWidgets.QWidgetAction(self.tool_layout)
        # self.action3.setText("Hard")
        # self.tool_layout.addAction(self.action3)
        # self.action3.triggered.connect(self.on_hard_released)

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

        self.tb_spacer1.setObjectName("spacer")
        self.tb_spacer2.setObjectName("spacer")
        self.tb_spacer3.setObjectName("spacer")
        self.tb_spacer4.setObjectName("spacer")
        self.tb_spacer5.setObjectName("spacer")
        # btns = self.tool_layout.findChildren(QToolButton)
        # for bt in btns:
        #     bt.setObjectName(bt.text().lower())
        # self.toolbar.setStyleSheet("QToolButton { width: 170%; margin: 5px 10px}")
        # self.central_layout.addWidget(self.toolbar,3,0,1,2)
        # self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)

        self.central_layout.addWidget(self.tool_layout,0, 0, 1, 2)
        self.finish = QMessageBox()

        for i in range(self.central_layout.count()):
            item = self.central_layout.itemAt(i)
            widget = item.widget()
            row, col, row_span, col_span = self.central_layout.getItemPosition(i)

            if widget:
                print(
                    f"  Cell [{row}, {col}] (span: {row_span}x{col_span}): {widget.objectName() or widget.__class__.__name__}"
                )
            else:
                print(f"  Cell [{row}, {col}]: Empty or spacer")

    def setWindowStyle(self, style):
        self.text_display.document().setDefaultStyleSheet(style[1])
        self.text_display.setHtmlText()
        super().setStyleSheet(style[0])
        # print(styleSheet)

    def set_statistics_mode(self, state: bool):
        if state:
            self.chart.show_overlay()
            self.text_display.hide()
        else:
            self.chart.hide()
            self.text_display.show()

    def on_show_statistics(self, data):
        self.chart.update_data(data)
        self.set_statistics_mode(True)

    @Slot()
    def on_stats_display(self, speed, typing_time):
        self.finish.setText(
            f"CPM - {speed:.2f} chars per minute\nTime - {typing_time:.2f} seconds"
        )
        # speed_lb = QLabel(f'CPM - {speed}', finish)
        self.finish.resize(500, 500)
        self.finish.exec()

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

    @Slot()
    def toolbutton_activate(self, name, isactive):
        pass
        # tb = self.toolbar.findChild(QtWidgets.QToolButton, name)

        # tb.setProperty("isactive", isactive)

        # tb.style().unpolish(tb)  # Обновляем стиль
        # tb.style().polish(tb)
        # tb.update()

    def on_key_theme_switch(self, style):
        self.key_theme_switch.emit()
        self.text_display.setFocus()
