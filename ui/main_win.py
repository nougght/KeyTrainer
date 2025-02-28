from PySide6 import QtWidgets, QtCore, QtGui, QtSvg
from ui.my_widgets import KeyWidget, KeyTextEdit, KeyProgressDisplay
import control.data_control as dt
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
        self.data = dt.KeyTrainerData()
        self.resize(700,500)

        # self.setWindowIcon(QtGui.QIcon("resources/keyIc (2).ico"))

        self.setWindowTitle("Key Trainer")
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_layout = QtWidgets.QGridLayout()
        self.central_widget.setLayout(self.central_layout)

        self.close_butt = QtWidgets.QPushButton("exit")
        self.close_butt.setFlat(True)
        self.close_butt.setObjectName("exitButton")
        self.close_butt.clicked.connect(self.on_exit_released)
        self.central_layout.addWidget(self.close_butt, 0, 1, QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop)

        self.theme_switch_button = QtWidgets.QPushButton("Поменять тему")
        self.central_layout.addWidget(self.theme_switch_button, 10, 0, QtCore.Qt.AlignmentFlag.AlignLeft)

        self.toolbar = QtWidgets.QToolBar()
        self.tb_spacer1 = QtWidgets.QWidget()

        self.tb_spacer1.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding,QtWidgets.QSizePolicy.Policy.MinimumExpanding,)
        self.toolbar.addWidget(self.tb_spacer1)

        self.rus_action = QtWidgets.QWidgetAction(self.toolbar)
        self.rus_action.setText("Russian")
        self.toolbar.addAction(self.rus_action)
        self.rus_action.triggered.connect(self.on_rus_released)

        self.eng_action = QtWidgets.QWidgetAction(self.toolbar)
        self.eng_action.setText("English")
        self.toolbar.addAction(self.eng_action)
        self.eng_action.triggered.connect(self.on_eng_released)

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
        self.text_display.key_press_release.connect(self.on_key_switch)
        self.text_display.finished.connect(self.on_finished)

        self.text_display.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Expanding)

        self.char_pos_label = KeyProgressDisplay(1)
        self.central_layout.addWidget(self.char_pos_label, 1, 0, QtCore.Qt.AlignmentFlag.AlignCenter)

        self.text_display.textSizeChanged.connect(self.char_pos_label.reset)
        self.text_display.cursorPositionChanged.connect(self.char_pos_label.on_inc_progress)
        self.text_display.cursorPositionChanged.connect(lambda : self.progress_bar.setValue(self.text_display.get_progress()))
        self.text_display.typo.connect(self.char_pos_label.on_typo)

        self.central_layout.addWidget(self.text_display, 2, 0, 1, 2)
        self.vert_spacer_1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.vert_spacer_2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.vert_spacer_3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)

        self.central_layout.addItem(self.vert_spacer_1, 0, 0, 1, 2)
        self.central_layout.addItem(self.vert_spacer_2, 3, 0, 1, 2)
        self.central_layout.addItem(self.vert_spacer_3, 9, 0, 1, 2)
        print(self.central_layout.rowCount())
        print(self.central_layout.columnCount())
        print(self.central_layout.itemAt(0))

        for i in range(4):
            keys_layout = QtWidgets.QHBoxLayout()
            for k in self.data.keys_en[i]:
                key = KeyWidget(k.upper())
                key.setObjectName(k)
                self.key_theme_switch.connect(key.on_theme_switch)
                keys_layout.addWidget(key,alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
            self.central_layout.addLayout(keys_layout, i + 4, 0, 1, 2, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        keys_layout = QtWidgets.QHBoxLayout()
        key = KeyWidget(self.data.keys_en[4][0])
        key.setObjectName("space")
        self.key_theme_switch.connect(key.on_theme_switch)
        keys_layout.addWidget(key, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.central_layout.addLayout(keys_layout, 8, 0, 1, 2)
        keys = self.central_widget.findChildren(KeyWidget)
        print(len(keys))

    def on_key_switch(self, ch, isPress):
        if ch == ' ':
            ch = 'space'
        wid = self.central_widget.findChildren(KeyWidget, ch.lower())
        print(len(wid))
        wid[0].set_active(isPress)

    def setStyleSheet(self, styleSheet):
        print("yoooooo")
        super().setStyleSheet(styleSheet)
        print(styleSheet)
    @QtCore.Slot()
    def on_finished(self):
        self.char_pos_label.on_inc_progress()
        finish = QtWidgets.QMessageBox(parent = self, text = "Perfect!")
        finish.resize(200,200)
        finish.exec()

    @QtCore.Slot()
    def on_exit_released(self):
        print("exit")
        self.close()

    @QtCore.Slot()
    def on_rus_released(self):
        self.language_change.emit("russian")

    @QtCore.Slot()
    def on_eng_released(self):
        self.language_change.emit("english")

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
        if isactive:
            tb.setStyleSheet("border: 5px solid #707070; font: 700 45px;")
        else:
            tb.setStyleSheet(
                "QToolbutton { border: 2px solid transparent;} QToolButton:hover{ border: 2px solid #707070;}"
            )

    def on_key_theme_switch(self, style):
        self.key_theme_switch.emit()
        self.text_display.setFocus()
