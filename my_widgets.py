from PySide6.QtWidgets import QDialog, QLabel, QComboBox, QTextEdit, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt
from PySide6 import QtCore, QtGui, QtWidgets
from my_data import KeyTrainerData
import time, os, sys


def resource_path(relative_path):
    """Get the absolute path to the resource, works for dev and for PyInstaller"""
    if hasattr(sys, "_MEIPASS"):
        # Если приложение запущено из собранного exe
        base_path = sys._MEIPASS
    else:
        # Если приложение запущено из исходного кода
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



with open(resource_path("dark.qss"), "r") as f:
    dark_stylesheet = f.read()

with open(resource_path("style.qss"), "r") as f:
    light_stylesheet = f.read()

class StarterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Запуск программы")
        self.resize(350, 300)
        with open(resource_path("theme.txt"), "r") as f:
            self.is_dark_theme = True if f.read() == "Dark" else False
        self.setStyleSheet(dark_stylesheet if self.is_dark_theme else light_stylesheet)
        self.vlayout = QVBoxLayout(self)

        self.profile_box = QComboBox()
        self.profile_box.addItem("Профиль 1")
        self.vlayout.addWidget(self.profile_box)

        self.accept_but = QPushButton("Войти")
        self.accept_but.clicked.connect(self.on_accept)
        self.vlayout.addWidget(self.accept_but, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.theme_switch = QPushButton("Поменять тему")
        self.theme_switch.clicked.connect(self.on_theme_switch)
        self.vlayout.addWidget(self.theme_switch, alignment=Qt.AlignmentFlag.AlignLeft)

    @QtCore.Slot()
    def on_accept(self):
        time.sleep(0.3)
        self.accept()

    @QtCore.Slot()
    def on_theme_switch(self):
        self.is_dark_theme = not self.is_dark_theme
        print(self.is_dark_theme)
        with open(resource_path("theme.txt"), "w") as f:
            if self.is_dark_theme is True:
                f.write("Dark")
                self.setStyleSheet(dark_stylesheet)
            else:
                f.write("Light")
                self.setStyleSheet(light_stylesheet)


class KeyWidget(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(50, 50)

    def set_active(self, active):
        style = (
            "background: #090f1b; border: 2px solid #88C0D0; " if active else "background: #2E3440; color: #ECEFF4; border: 1px solid #4C566A;"
        )
        self.setStyleSheet(f"QLabel  {{ {style} }}")


class KeyTextEdit(QTextEdit):
    key_press_release = QtCore.Signal(str, bool)
    finished = QtCore.Signal()

    def __init__(self, text = ''):
        super().__init__()

        # Инициализация формата подчёркивания
        self.underline_format = QtGui.QTextCharFormat()
        self.underline_format.setUnderlineStyle(
            QtGui.QTextCharFormat.UnderlineStyle.SingleUnderline
        )
        self.underline_format.setUnderlineColor(QtGui.QColor("#0d2b96"))

        self.passed_format = QtGui.QTextCharFormat()
        self.passed_format.setBackground(QtGui.QColor("#36ee77"))

        self.setReadOnly(True)
        self.setText(text)
        # self.text_display.setFixedHeight(150)
        self.setFont(QtGui.QFont("Consolas", 35, 500))
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.cursorForPosition(QtCore.QPoint(0, 0))
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # self.setFrameStyle(
        #     QtWidgets.QFrame.Box| QtWidgets.QFrame.Plain
        # )
        # Прямоугольник без тени
        self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)  # Панель с объёмной тенью

        cursor = self.textCursor()

        # Выделить текущий символ
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.Right, QtGui.QTextCursor.MoveMode.KeepAnchor)
        cursor.mergeCharFormat(self.underline_format)
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.Left)
        self.setTextCursor(cursor)

    def setText(self, text):

        cursor = self.textCursor()
        cursor.setCharFormat(QtGui.QTextCharFormat())
        self.setTextCursor(cursor)
        super().setText(text)
        cursor = self.textCursor()
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.Start)
        # Выделить текущий символ
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.Right, QtGui.QTextCursor.MoveMode.KeepAnchor)
        cursor.mergeCharFormat(self.underline_format)
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.Left)
        self.setTextCursor(cursor)

    def keyPressEvent(self, event):
        ch = event.text()

        if event.key() != QtCore.Qt.Key.Key_Space:
            self.key_press_release.emit(ch, True)

        cursor = self.textCursor()
        print(cursor.position())
        print(ch.lower())
        if event.key() == QtCore.Qt.Key.Key_Enter:
            pass
        else:
            print(len(self.toPlainText()), cursor.position())

            if event.text() == self.toPlainText()[cursor.position()]:

                print("perfect")

                cursor.movePosition(
                    QtGui.QTextCursor.MoveOperation.Right,
                    QtGui.QTextCursor.MoveMode.KeepAnchor,
                )
                cursor.setCharFormat(self.passed_format)
                cursor.movePosition(QtGui.QTextCursor.MoveOperation.Left)
                if len(self.toPlainText()) - 1 == cursor.position():
                    self.keyReleaseEvent(event)
                    self.finished.emit()
                cursor.movePosition(QtGui.QTextCursor.MoveOperation.Right)
                cursor.movePosition(
                    QtGui.QTextCursor.MoveOperation.Right,
                    QtGui.QTextCursor.MoveMode.KeepAnchor,
                )
                cursor.mergeCharFormat(self.underline_format)
                cursor.movePosition(QtGui.QTextCursor.MoveOperation.Left)
                self.setTextCursor(cursor)

                print()

        return super().keyPressEvent(event) if event.key() != Qt.Key.Key_Space else None

        # format = cursor.charFormat()
        # format.setUnderlineStyle(QtGui.QTextCharFormat.UnderlineStyle.SingleUnderline)
        # format.setUnderlineColor("#00c455")  # Подсветка фона
        # format.setBackground(QtCore.Qt.yellow)
        # cursor.setCharFormat(format)
        # self.text_display.setTextCursor(cursor)
        # self.text_display.setCursorPosition(self.text_display.cursorPosition() + 1)

    def keyReleaseEvent(self, event):
        ch = event.text()
        if event.key() == QtCore.Qt.Key.Key_Space:
            return None
        else:
            self.key_press_release.emit(ch, False)

        return super().keyPressEvent(event)

    def mousePressEvent(self, e):
        pass
        # return super().mousePressEvent(e)
    def mouseDoubleClickEvent(self, e):
        pass
        # return super().mouseDoubleClickEvent(e)
    def mouseMoveEvent(self, e):
        pass
        # return super().mouseMoveEvent(e)
