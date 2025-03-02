from PySide6.QtWidgets import QDialog, QLabel, QComboBox, QTextEdit, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt
from PySide6 import QtCore, QtGui, QtWidgets
import control.data_control as dt
from control.settings_control import SettingControl
import time, os, sys


class StarterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Запуск программы")
        self.resize(350, 300)

        self.selected_profile = None

        self.vlayout = QVBoxLayout(self)

        self.profile_box = QComboBox()
        self.profile_box.addItem("Профиль 1")
        self.vlayout.addWidget(self.profile_box)
        self.profile_box.addItem("Профиль 2")
        self.vlayout.addWidget(self.profile_box)
        self.profile_box.addItem("Профиль 3")
        self.vlayout.addWidget(self.profile_box)

        self.accept_but = QPushButton("Войти")
        self.accept_but.clicked.connect(self.accept)
        self.vlayout.addWidget(self.accept_but, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.theme_switch_button = QPushButton("Поменять тему")
        self.vlayout.addWidget(self.theme_switch_button, alignment=Qt.AlignmentFlag.AlignLeft)

    def accept(self):
        self.selected_profile = None
        return super().accept()
    
    def get_selected_profile(self):
        return self.selected_profile
    
    @QtCore.Slot()
    def on_accept(self):
        time.sleep(0.3)
        self.accept()


class KeyWidget(QLabel):
    style = ["background: #88C0D0; color: #090f1b; border: 2px solid #090f1b;",
             "background: #090f1b; border: 2px solid #88C0D0; color: #88C0D0;"]
    def __init__(self, text, parent=None, isdark=False):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFont(QtGui.QFont("consolas", 50, 500))

    def set_active(self, active):
        self.setStyleSheet(f"KeyWidget  {{ {self.style[active]} }}")

    @QtCore.Slot()
    def on_theme_switch(self):
        self.style = [self.style[1], self.style[0]]
        self.setStyleSheet(f"KeyWidget  {{ {self.style[0]} }}")


class KeyProgressDisplay(QLabel):
    def __init__(self, total = 0):
        self.total = total
        self.progress = 0
        self.typos = 0
        super().__init__(f"{self.progress}/{self.total} ({self.progress / self.total:.1%})\t Ошибок: {self.typos}")

    def reset(self, new_total = 0):
        self.total = new_total
        self.progress = 0
        self.typos = 0
        self.setText(
            f"{self.progress}/{self.total} ({self.progress / self.total:.1%})\t Ошибок: {self.typos}"
        )

    @QtCore.Slot()
    def on_inc_progress(self):
        self.progress += 1
        self.setText(
            f"{self.progress}/{self.total} ({self.progress / self.total:.1%})\t Ошибок: {self.typos}"
        )

    @QtCore.Slot()
    def on_typo(self):
        self.typos += 1
        self.setText(
            f"{self.progress}/{self.total} ({self.progress / self.total:.1%})\t Ошибок: {self.typos}"
        )


class KeyTextEdit(QTextEdit):
    key_press_release = QtCore.Signal(str, bool )
    textSizeChanged = QtCore.Signal(int)
    typing_start = QtCore.Signal()
    finished = QtCore.Signal()
    typo = QtCore.Signal()

    def __init__(self):
        super().__init__()

        # Инициализация формата подчёркивания
        self.underline_format = QtGui.QTextCharFormat()
        self.underline_format.setUnderlineStyle(
            QtGui.QTextCharFormat.UnderlineStyle.SingleUnderline
        )
        self.underline_format.setUnderlineColor(QtGui.QColor("#9480eb"))

        self.passed_format = QtGui.QTextCharFormat()
        self.passed_format.setBackground(QtGui.QColor("#279346"))

        self.setReadOnly(True)
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Preferred)
        # self.text_display.setFixedHeight(150)
        # self.setFixedHeight(200)
        self.setFont(QtGui.QFont("Consolas", 35, 500))
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.cursorForPosition(QtCore.QPoint(0, 0))
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # self.setFrameStyle(
        #     QtWidgets.QFrame.Box| QtWidgets.QFrame.Plain
        # )
        # Прямоугольник без тени
        # self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)  # Панель с объёмной тенью

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
        self.textSizeChanged.emit(len(text))

    def get_progress(self):
        cursor = self.textCursor()
        return int(cursor.position() / len(self.toPlainText()) * 100)
    
    def keyPressEvent(self, event):
        ch = event.text()

        self.key_press_release.emit(ch, True)

        cursor = self.textCursor()
        if cursor.position() == 0:
            self.typing_start.emit()

        print(cursor.position(), 'pos')
        print(ch.lower())
        if event.key() == QtCore.Qt.Key.Key_Enter or event.key() == QtCore.Qt.Key.Key_Shift:
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
            else:
                self.typo.emit()

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
        self.key_press_release.emit(ch, False)

        return super().keyPressEvent(event) if event.key() != QtCore.Qt.Key.Key_Space else None

    def mousePressEvent(self, e):
        pass
        # return super().mousePressEvent(e)
    def mouseDoubleClickEvent(self, e):
        pass
        # return super().mouseDoubleClickEvent(e)
    def mouseMoveEvent(self, e):
        pass
        # return super().mouseMoveEvent(e)
