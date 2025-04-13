from PySide6 import QtWidgets, QtCore, QtGui, QtSvg
from ui.my_widgets import KeyWidget, KeyTextEdit, KeyProgressDisplay, KeyboardWidget, RadioList
from control.settings_control import SettingControl

import time
import random as rd


class MainWindow(QtWidgets.QMainWindow):
    key_theme_switch = QtCore.Signal()
    difficulty_change = QtCore.Signal(str)
    language_change = QtCore.Signal(str)
    mod_change = QtCore.Signal(str)
    def __init__(self):
        super().__init__()
        self.resize(700,500)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,  # Растягивается по горизонтали
            QtWidgets.QSizePolicy.Expanding,  # Растягивается по вертикали
        )

        # self.setWindowIcon(QtGui.QIcon("resources/keyIc (2).ico"))

        self.setWindowTitle("Key Trainer")
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_layout = QtWidgets.QGridLayout()
        self.central_widget.setLayout(self.central_layout)

        self.mBar = QtWidgets.QMenuBar()
        self.mBar.setNativeMenuBar(True)
        self.mBar.addAction("Профиль")
        self.mBar.addAction("Настройки")
        self.mBar.addAction("Статистика")

        self.right_widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(self.right_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        self.minimize_btn = QtWidgets.QPushButton("—")
        self.minimize_btn.setObjectName("minimizeButton")
        self.minimize_btn.pressed.connect(self.showMinimized)
        self.close_btn = QtWidgets.QPushButton("✕")
        self.close_btn.setObjectName("exitButton")
        self.close_btn.pressed.connect(self.on_exit_released)

        layout.addWidget(self.minimize_btn)
        layout.addWidget(self.close_btn)

        # Добавляем виджет в правый угол меню-бара
        self.mBar.setCornerWidget(self.right_widget)

        self.mb_spacer1 = QtWidgets.QWidget()
        self.mb_spacer1.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self.setMenuBar(self.mBar)

        lang_group = QtWidgets.QButtonGroup()
        ru_btn = QtWidgets.QRadioButton()
        ru_btn.setText('yo')
        en_btn = QtWidgets.QRadioButton()
        en_btn.setText('oy')

        lang_group.addButton(ru_btn, id=0)
        lang_group.addButton(en_btn, id=1)
        self.central_layout.addWidget(ru_btn)
        self.central_layout.addWidget(en_btn)

        self.theme_switch_button = QtWidgets.QPushButton("Поменять тему")
        self.theme_switch_button.setObjectName("themes")
        # self.theme_switch_button.setIcon(QtGui.QIcon("data/themes.svg"))
        self.central_layout.addWidget(self.theme_switch_button, 10, 0, QtCore.Qt.AlignmentFlag.AlignLeft)

        self.reset_button = QtWidgets.QPushButton("⟳")
        self.reset_button.setObjectName("reset")
        self.central_layout.addWidget(self.reset_button, 10, 1, QtCore.Qt.AlignmentFlag.AlignRight)

        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.layout().setSpacing(0)
        self.toolbar.layout().setContentsMargins(0, 0, 0, 0)
        self.tb_spacer1 = QtWidgets.QWidget()

        self.tb_spacer1.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding,QtWidgets.QSizePolicy.Policy.MinimumExpanding,)
        self.toolbar.addWidget(self.tb_spacer1)

        self.lang_combo = QtWidgets.QComboBox()
        self.lang_combo.addItem('Russian')
        self.lang_combo.addItem('English')
        self.lang_combo.currentIndexChanged.connect(lambda index: self.language_change.emit(self.lang_combo.itemText(index).lower()))
        self.toolbar.addWidget(self.lang_combo)

        # self.rus_action = QtWidgets.QWidgetAction(self.toolbar)
        # self.rus_action.setText("Russian")
        # self.toolbar.addAction(self.rus_action)
        # self.rus_action.triggered.connect(self.on_rus_released)

        # self.eng_action = QtWidgets.QWidgetAction(self.toolbar)
        # self.eng_action.setText("English")
        # self.toolbar.addAction(self.eng_action)
        # self.eng_action.triggered.connect(self.on_eng_released)

        self.tb_spacer2 = QtWidgets.QWidget()
        self.tb_spacer2.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self.toolbar.addWidget(self.tb_spacer2)

        self.words_action = QtWidgets.QWidgetAction(self.toolbar)
        self.words_action.setText("Words")
        self.toolbar.addAction(self.words_action)
        self.words_action.triggered.connect(self.on_words_released)

        self.text_action = QtWidgets.QWidgetAction(self.toolbar)
        self.text_action.setText("Text")
        self.toolbar.addAction(self.text_action)
        self.text_action.triggered.connect(self.on_text_released)

        self.tb_spacer3 = QtWidgets.QWidget()
        self.tb_spacer3.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self.toolbar.addWidget(self.tb_spacer3)

        mode_list = RadioList()
        mode_list.add_items(["Words", "Text"])
        self.toolbar.addWidget(mode_list)
        diff_list = RadioList()
        diff_list.add_items(["Easy", "Normal", "Hard"])
        # list_widget = QtWidgets.QListWidget()
        # list_widget.setFlow(list_widget.Flow.LeftToRight)
        # list_widget.setWrapping(True)
        # list_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # list_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # list_widget.setSizeAdjustPolicy(QtWidgets.QListWidget.SizeAdjustPolicy.AdjustToContents)
        # list_widget.addItems(["Easy", "Normal", "Hard"])
        # list_widget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        # list_widget.adjustSize()
        # list_widget.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        # list_widget.setSizePolicy(
        #     QtWidgets.QSizePolicy.Policy.Fixed,
        #     QtWidgets.QSizePolicy.Policy.Fixed,
        # )
        self.toolbar.addWidget(diff_list)

        self.action1 = QtWidgets.QWidgetAction(self.toolbar)
        self.action1.setText("Easy")
        self.toolbar.addAction(self.action1)
        self.action1.triggered.connect(self.on_easy_released)

        self.action2 = QtWidgets.QWidgetAction(self.toolbar)
        self.action2.setText("Normal")
        self.toolbar.addAction(self.action2)
        self.action2.triggered.connect(self.on_mid_released)

        self.action3 = QtWidgets.QWidgetAction(self.toolbar)
        self.action3.setText("Hard")
        self.toolbar.addAction(self.action3)
        self.action3.triggered.connect(self.on_hard_released)

        self.tb_spacer4 = QtWidgets.QWidget()
        self.tb_spacer4.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.toolbar.addWidget(self.tb_spacer4)
        self.tb_spacer5 = QtWidgets.QWidget()
        self.tb_spacer5.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Expanding)
        # self.toolbar.addWidget(self.tb_spacer5)

        self.tb_spacer1.setObjectName("spacer")
        self.tb_spacer2.setObjectName("spacer")
        self.tb_spacer3.setObjectName("spacer")
        self.tb_spacer4.setObjectName("spacer")
        self.tb_spacer5.setObjectName("spacer")
        btns = self.toolbar.findChildren(QtWidgets.QToolButton)
        for bt in btns:
            bt.setObjectName(bt.text().lower())
        self.toolbar.setStyleSheet("QToolButton { width: 170%; margin: 5px 10px}")
        self.addToolBar(QtCore.Qt.ToolBarArea.LeftToolBarArea, self.toolbar)
        self.progress_bar = QtWidgets.QProgressBar(minimum=0, maximum=100)
        self.central_layout.addWidget(self.progress_bar, 1, 1, QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.progress_bar.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        # self.progress_bar.setTextVisible(False)

        self.text_display = KeyTextEdit()

        self.text_display.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Expanding)

        self.char_pos_label = KeyProgressDisplay(1)
        self.central_layout.addWidget(self.char_pos_label, 1, 0, QtCore.Qt.AlignmentFlag.AlignCenter)

        self.central_layout.addWidget(self.text_display, 2, 0, 1, 2)
        self.vert_spacer_1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.vert_spacer_2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.vert_spacer_3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)

        self.central_layout.addItem(self.vert_spacer_2, 3, 0, 1, 2)
        self.central_layout.addItem(self.vert_spacer_3, 9, 0, 1, 2)
        print(self.central_layout.rowCount())
        print(self.central_layout.columnCount())
        print(self.central_layout.itemAt(0))

        self.keyboard_widget = KeyboardWidget("english")
        print(self.keyboard_widget.size().height(), self.keyboard_widget.size().width())
        self.key_theme_switch.connect(self.keyboard_widget.on_key_theme_switch)
        self.central_layout.addWidget(self.keyboard_widget, 4, 0, 1, 2, alignment = QtCore.Qt.AlignmentFlag.AlignCenter)

        self.finish = QtWidgets.QMessageBox()
        button_box = self.finish.findChild(QtWidgets.QDialogButtonBox)
        if button_box:
            button_box.setCenterButtons(True)

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

    @QtCore.Slot()
    def on_stats_display(self, speed, typing_time):
        self.finish.setText(f'CPM - {speed:.2f} chars per minute\nTime - {typing_time:.2f} seconds')
        # speed_lb = QtWidgets.QLabel(f'CPM - {speed}', finish)
        self.finish.resize(500, 500)
        self.finish.exec()

    @QtCore.Slot()
    def on_exit_released(self):
        print("exit")
        self.close()

    # @QtCore.Slot()
    # def on_rus_released(self):
    #     self.language_change.emit("russian")

    # @QtCore.Slot()
    # def on_eng_released(self):
    #     self.language_change.emit("english")

    @QtCore.Slot()
    def on_words_released(self):
        self.mod_change.emit("words")

    @QtCore.Slot()
    def on_text_released(self):
        self.mod_change.emit("text")

    @QtCore.Slot()
    def on_easy_released(self):
        self.difficulty_change.emit("easy")

    @QtCore.Slot()
    def on_mid_released(self):
        self.difficulty_change.emit("normal")

    @QtCore.Slot()
    def on_hard_released(self):
        self.difficulty_change.emit("hard")

    @QtCore.Slot()
    def toolbutton_activate(self, name, isactive):
        tb = self.toolbar.findChild(QtWidgets.QToolButton, name)

        tb.setProperty("isactive", isactive)

        tb.style().unpolish(tb)  # Обновляем стиль
        tb.style().polish(tb)
        tb.update()

    def on_key_theme_switch(self, style):
        self.key_theme_switch.emit()
        self.text_display.setFocus()
