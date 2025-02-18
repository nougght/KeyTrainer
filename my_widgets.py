from PySide6.QtWidgets import QDialog, QLabel, QComboBox, QTextEdit, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt
from PySide6 import QtCore, QtGui, QtWidgets
import my_data as dt
import time, os, sys


class StarterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Запуск программы")
        self.resize(350, 300)
        
        self.setStyleSheet(dt.dark_stylesheet if dt.theme == "Dark" else dt.light_stylesheet)
        self.vlayout = QVBoxLayout(self)

        self.profile_box = QComboBox()
        self.profile_box.addItem("Профиль 1")
        self.vlayout.addWidget(self.profile_box)
        self.profile_box.addItem("Профиль 2")
        self.vlayout.addWidget(self.profile_box)
        self.profile_box.addItem("Профиль 3")
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
        dt.switch_theme()
        if dt.theme == "Dark":
            self.setStyleSheet(dt.dark_stylesheet)
        else:
            self.setStyleSheet(dt.light_stylesheet)


class KeyWidget(QLabel):
    light = ["background: #88C0D0; color: #090f1b; border: 2px solid #090f1b;","background: #090f1b; border: 2px solid #88C0D0; color: #88C0D0;"]
    dark = [light[1], light[0]]
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QtGui.QFont("consolas", 50, 500))


        
    def set_active(self, active):
        style = (
            self.light[active]
            if dt.theme == "Light"
            else self.dark[active]
        )
        print(style, active, self.dark[0])
        self.setStyleSheet(f"KeyWidget  {{ {style} }}")
    
    @QtCore.Slot()
    def on_theme_switch(self, th_st):
        self.setStyleSheet(f"KeyWidget  {{ {th_st[0]} }}")


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
    key_press_release = QtCore.Signal(str, bool)
    textSizeChanged = QtCore.Signal(int)
    finished = QtCore.Signal()
    typo = QtCore.Signal()

    def __init__(self, text = ''):
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
        self.setText(text)
        # self.text_display.setFixedHeight(150)
        self.setFont(QtGui.QFont("Consolas", 35, 500))
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.cursorForPosition(QtCore.QPoint(0, 0))
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.setFrameStyle(
            QtWidgets.QFrame.Box| QtWidgets.QFrame.Plain
        )
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

    def keyPressEvent(self, event):
        ch = event.text()

        self.key_press_release.emit(ch, True)

        cursor = self.textCursor()
        print(cursor.position())
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
