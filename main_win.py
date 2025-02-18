from PySide6 import QtWidgets, QtCore, QtGui, QtSvg
from my_widgets import KeyWidget, KeyTextEdit
from my_data import KeyTrainerData

import random as rd

import sys
import os


def resource_path(relative_path):
    """Get the absolute path to the resource, works for dev and for PyInstaller"""
    if hasattr(sys, "_MEIPASS"):
        # Если приложение запущено из собранного exe
        base_path = sys._MEIPASS
    else:
        # Если приложение запущено из исходного кода
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = KeyTrainerData()
        self.resize(700,500)

        # self.setWindowIcon(QtGui.QIcon("resources/keyIc (2).ico"))
        with open(resource_path("style.qss"), "r") as f:
            self.light_stylesheet = f.read()
        with open(resource_path("dark.qss"), "r") as f:
            self.dark_stylesheet = f.read()

        with open(resource_path("theme.txt"), "r") as f:
            self.is_dark_theme = True if f.read() == "Dark" else False

        if self.is_dark_theme:
            self.setStyleSheet(self.dark_stylesheet)

        self.setWindowTitle("Key Trainer")
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_layout = QtWidgets.QGridLayout()
        self.central_widget.setLayout(self.central_layout)

        self.close_butt = QtWidgets.QPushButton("Exit")
        self.close_butt.setFlat(True)
        self.close_butt.setObjectName("exitButton")
        self.close_butt.clicked.connect(self.on_exit_released)
        self.central_layout.addWidget(self.close_butt, 0, 1, QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop)

        self.theme_switch = QtWidgets.QPushButton("Поменять тему")
        self.theme_switch.clicked.connect(self.on_theme_switch)
        self.central_layout.addWidget(self.theme_switch, 7, 0, QtCore.Qt.AlignmentFlag.AlignLeft)

        self.toolbar = QtWidgets.QToolBar()
        self.action1 = QtWidgets.QWidgetAction(self.toolbar)
        self.action1.setText("Easy")
        self.toolbar.addAction(self.action1)
        self.action1.triggered.connect(self.on_easy_released)

        self.action2 = QtWidgets.QWidgetAction(self.toolbar)
        self.action2.setText("Middle")
        self.toolbar.addAction(self.action2)
        self.action2.triggered.connect(self.on_mid_released)

        self.action3 = QtWidgets.QWidgetAction(self.toolbar)
        self.action3.setText("Hard")
        self.toolbar.addAction(self.action3)
        self.action3.triggered.connect(self.on_hard_released)

        self.addToolBar(QtCore.Qt.ToolBarArea.LeftToolBarArea, self.toolbar)
        self.text_display = KeyTextEdit()
        self.text_display.key_press_release.connect(self.on_key_switch)
        self.text_display.finished.connect(self.on_finished)

        self.central_layout.addWidget(self.text_display, 1, 0, 1, 2)
        self.vert_spacer_1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.vert_spacer_2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.vert_spacer_3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)

        self.central_layout.addItem(self.vert_spacer_1, 0, 0, 1, 2)
        self.central_layout.addItem(self.vert_spacer_2, 2, 0, 1, 2)
        self.central_layout.addItem(self.vert_spacer_3, 8, 0, 1, 2)
        print(self.central_layout.rowCount())
        print(self.central_layout.columnCount())
        print(self.central_layout.itemAt(0))

        for i in range(4):
            keys_layout = QtWidgets.QHBoxLayout()
            for k in self.data.keys_en[i]:
                key = KeyWidget(k.upper())
                key.setObjectName(k)
                keys_layout.addWidget(key,alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
            self.central_layout.addLayout(keys_layout, i + 3, 0, 1, 2, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)

        keys = self.central_widget.findChildren(KeyWidget)
        print(len(keys))

        self.action1.trigger()
        

    def on_key_switch(self, ch, isPress):
        wid = self.findChildren(KeyWidget, ch.lower())
        wid[0].set_active(isPress)

    def on_finished(self):
        print("kfdlkajlksdj")
        finish = QtWidgets.QMessageBox(parent = self, text = "Perfect!")
        finish.resize(100,100)
        finish.exec()

    @QtCore.Slot()
    def on_exit_released(self):
        print("exit")
        self.close()

    @QtCore.Slot()
    def on_easy_released(self):
        self.text_display.setText(self.data.easy_text[rd.randint(0, len(self.data.easy_text) - 1)])

    @QtCore.Slot()
    def on_mid_released(self):
        self.text_display.setText(self.data.mid_text[rd.randint(0, len(self.data.mid_text) - 1)])

    @QtCore.Slot()
    def on_hard_released(self):
        self.text_display.setText(self.data.hard_text[rd.randint(0, len(self.data.hard_text) - 1)])

    @QtCore.Slot()
    def on_theme_switch(self):
        self.is_dark_theme = not self.is_dark_theme
        print(self.is_dark_theme)
        with open(resource_path("theme.txt"), "w") as f:
            if self.is_dark_theme is True:
                f.write("Dark")
                self.setStyleSheet(self.dark_stylesheet)
            else:
                f.write("Light")
                self.setStyleSheet(self.light_stylesheet)
