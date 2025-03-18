from PySide6 import QtWidgets, QtCore, QtGui, QtSvg
from ui.my_widgets import KeyWidget, KeyTextEdit, KeyProgressDisplay, KeyboardWidget
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

        self.close_butt = QtWidgets.QPushButton("exit")
        self.close_butt.setFlat(True)
        self.close_butt.setObjectName("exitButton")
        self.close_butt.clicked.connect(self.on_exit_released)
        self.central_layout.addWidget(self.close_butt, 0, 1, QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop)

        self.theme_switch_button = QtWidgets.QPushButton("Поменять тему")
        self.central_layout.addWidget(self.theme_switch_button, 10, 0, QtCore.Qt.AlignmentFlag.AlignLeft)

        self.reset_button = QtWidgets.QPushButton("⟳")
        self.reset_button.setObjectName("reset")
        self.central_layout.addWidget(self.reset_button, 10, 1, QtCore.Qt.AlignmentFlag.AlignRight)

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

        self.text_display.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Expanding)

        self.char_pos_label = KeyProgressDisplay(1)
        self.central_layout.addWidget(self.char_pos_label, 1, 0, QtCore.Qt.AlignmentFlag.AlignCenter)


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

        self.keyboard_widget = KeyboardWidget("english")
        print(self.keyboard_widget.size().height(), self.keyboard_widget.size().width())
        self.key_theme_switch.connect(self.keyboard_widget.on_key_theme_switch)
        self.central_layout.addWidget(self.keyboard_widget, 4, 0, 1, 2, alignment = QtCore.Qt.AlignmentFlag.AlignCenter)


        self.finish = QtWidgets.QMessageBox()
        button_box = self.finish.findChild(QtWidgets.QDialogButtonBox)
        if button_box:
            button_box.setCenterButtons(True)

    def setStyleSheet(self, styleSheet):
        print("yoooooo")
        super().setStyleSheet(styleSheet)
        # print(styleSheet)

    @QtCore.Slot()
    def on_stats_display(self, speed, typing_time):
        self.char_pos_label.on_inc_progress()
        self.progress_bar.setValue(100)
        self.finish.setText(f'CPM - {speed:.2f} chars per minute\nTime - {typing_time:.2f} seconds')
        # speed_lb = QtWidgets.QLabel(f'CPM - {speed}', finish)
        self.finish.resize(500, 500)
        time.sleep(0.5)
        self.finish.exec()

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
