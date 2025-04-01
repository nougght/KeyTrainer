from PySide6.QtWidgets import QDialog, QLabel, QComboBox, QTextEdit, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt
from PySide6 import QtCore, QtGui, QtWidgets
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


class KeyWidget(QPushButton):
    styles = ["background: #88C0D0; color: #090f1b; border: 2px solid #090f1b;",
             "background: #090f1b; border: 2px solid #88C0D0; color: #88C0D0;"]

    def __init__(self, text, parent=None, isdark=False):
        super().__init__(text, parent)
        self.setMinimumSize(60, 60)  # Минимальный размер клавиши
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,  # Растягивается по горизонтали
            QtWidgets.QSizePolicy.Policy.Expanding,  # Растягивается по вертикали
        )
        # self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setProperty('pressed', True)
        self.setDisabled(True)
        # self.setDown(True)

    def set_active(self, active):
        self.setProperty("uncorrect", False)
        self.style().unpolish(self)  # Обновляем стиль
        self.style().polish(self)
        self.update()
        self.setDown(active)

    # def theme_switch(self):
    #     self.styles = [self.styles[1], self.styles[0]]
    #     self.setStyleSheet(f"KeyWidget  {{ {self.styles[0]} }}")

    def set_uncorrect(self):
        self.setProperty("uncorrect", True)
        self.style().unpolish(self)  # Обновляем стиль
        self.style().polish(self)
        self.update()
        # self.repaint()


class KeyboardWidget(QtWidgets.QWidget):
    keys_en = [
        [
            {"name": "key_`", "def": "`", "shift": "~"},
            {"name": "key_1", "def": "1", "shift": "!"},
            {"name": "key_2", "def": "2", "shift": "@"},
            {"name": "key_3", "def": "3", "shift": "#"},
            {"name": "key_4", "def": "4", "shift": "$"},
            {"name": "key_5", "def": "5", "shift": "%"},
            {"name": "key_6", "def": "6", "shift": "^"},
            {"name": "key_7", "def": "7", "shift": "&"},
            {"name": "key_8", "def": "8", "shift": "*"},
            {"name": "key_9", "def": "9", "shift": "("},
            {"name": "key_0", "def": "0", "shift": ")"},
            {"name": "key_-", "def": "-", "shift": "_"},
            {"name": "key_=", "def": "=", "shift": "+"},
            {"name": "key_BACKSPACE", "def": "BACKSPACE", "shift": "BACKSPACE"},
        ],
        [
            {"name": "key_TAB", "def": "TAB", "shift": "TAB"},
            {"name": "key_q", "def": "q", "shift": "Q"},
            {"name": "key_w", "def": "w", "shift": "W"},
            {"name": "key_e", "def": "e", "shift": "E"},
            {"name": "key_r", "def": "r", "shift": "R"},
            {"name": "key_t", "def": "t", "shift": "T"},
            {"name": "key_y", "def": "y", "shift": "Y"},
            {"name": "key_u", "def": "u", "shift": "U"},
            {"name": "key_i", "def": "i", "shift": "I"},
            {"name": "key_o", "def": "o", "shift": "O"},
            {"name": "key_p", "def": "p", "shift": "P"},
            {"name": "key_[", "def": "[", "shift": "{"},
            {"name": "key_]", "def": "]", "shift": "}"},
            {"name": "key_\\", "def": "\\", "shift": "|"},
        ],
        [
            {"name": "key_CAPS", "def": "CAPS", "shift": "CAPS"},
            {"name": "key_a", "def": "a", "shift": "A"},
            {"name": "key_s", "def": "s", "shift": "S"},
            {"name": "key_d", "def": "d", "shift": "D"},
            {"name": "key_f", "def": "f", "shift": "F"},
            {"name": "key_g", "def": "g", "shift": "G"},
            {"name": "key_h", "def": "h", "shift": "H"},
            {"name": "key_j", "def": "j", "shift": "J"},
            {"name": "key_k", "def": "k", "shift": "K"},
            {"name": "key_l", "def": "l", "shift": "L"},
            {"name": "key_;", "def": ";", "shift": ":"},
            {"name": "key_'", "def": "'", "shift": '"'},
            {"name": "key_ENTER", "def": "ENTER", "shift": "ENTER"},
        ],
        [
            {"name": "key_SHIFT", "def": "SHIFT", "shift": "SHIFT"},
            {"name": "key_z", "def": "z", "shift": "Z"},
            {"name": "key_x", "def": "x", "shift": "X"},
            {"name": "key_c", "def": "c", "shift": "C"},
            {"name": "key_v", "def": "v", "shift": "V"},
            {"name": "key_b", "def": "b", "shift": "B"},
            {"name": "key_n", "def": "n", "shift": "N"},
            {"name": "key_m", "def": "m", "shift": "M"},
            {"name": "key_,", "def": ",", "shift": "<"},
            {"name": "key_.", "def": ".", "shift": ">"},
            {"name": "key_/", "def": "/", "shift": "?"},
            {"name": "key_SHIFT", "def": "SHIFT", "shift": "SHIFT"},
        ],
        [
            {"name": "key_CTRL", "def": "CTRL", "shift": "CTRL"},
            {"name": "key_ALT", "def": "ALT", "shift": "ALT"},
            {"name": "key_SPACE", "def": " ", "shift": " "},
            {"name": "key_ALT", "def": "ALT", "shift": "ALT"},
            {"name": "key_CTRL", "def": "CTRL", "shift": "CTRL"},
        ],
    ]
    keys_ru = [
        [
            {"name": "key_ё", "def": "ё", "shift": "Ё"},
            {"name": "key_1", "def": "1", "shift": "1"},
            {"name": "key_2", "def": "2", "shift": "2"},
            {"name": "key_3", "def": "3", "shift": "3"},
            {"name": "key_4", "def": "4", "shift": "4"},
            {"name": "key_5", "def": "5", "shift": "5"},
            {"name": "key_6", "def": "6", "shift": "6"},
            {"name": "key_7", "def": "7", "shift": "7"},
            {"name": "key_8", "def": "8", "shift": "8"},
            {"name": "key_9", "def": "9", "shift": "9"},
            {"name": "key_0", "def": "0", "shift": "0"},
            {"name": "key_-", "def": "-", "shift": "-"},
            {"name": "key_+", "def": "+", "shift": "+"},
            {"name": "key_BACKSPACE", "def": "BACKSPACE", "shift": "BACKSPACE"},
        ],
        [
            {"name": "key_TAB", "def": "TAB", "shift": "TAB"},
            {"name": "key_й", "def": "й", "shift": "Й"},
            {"name": "key_ц", "def": "ц", "shift": "Ц"},
            {"name": "key_у", "def": "у", "shift": "У"},
            {"name": "key_к", "def": "к", "shift": "К"},
            {"name": "key_е", "def": "е", "shift": "Е"},
            {"name": "key_н", "def": "н", "shift": "Н"},
            {"name": "key_г", "def": "г", "shift": "Г"},
            {"name": "key_ш", "def": "ш", "shift": "Ш"},
            {"name": "key_щ", "def": "щ", "shift": "Щ"},
            {"name": "key_з", "def": "з", "shift": "З"},
            {"name": "key_х", "def": "х", "shift": "Х"},
            {"name": "key_ъ", "def": "ъ", "shift": "Ъ"},
            {"name": "key_\\", "def": "\\", "shift": "\\"},
        ],
        [
            {"name": "key_CAPS", "def": "CAPS", "shift": "CAPS"},
            {"name": "key_ф", "def": "ф", "shift": "Ф"},
            {"name": "key_ы", "def": "ы", "shift": "Ы"},
            {"name": "key_в", "def": "в", "shift": "В"},
            {"name": "key_а", "def": "а", "shift": "А"},
            {"name": "key_п", "def": "п", "shift": "П"},
            {"name": "key_р", "def": "р", "shift": "Р"},
            {"name": "key_о", "def": "о", "shift": "О"},
            {"name": "key_л", "def": "л", "shift": "Л"},
            {"name": "key_д", "def": "д", "shift": "Д"},
            {"name": "key_ж", "def": "ж", "shift": "Ж"},
            {"name": "key_э", "def": "э", "shift": "Э"},
            {"name": "key_ENTER", "def": "ENTER", "shift": "ENTER"},
        ],
        [
            {"name": "key_SHIFT1", "def": "SHIFT", "shift": "SHIFT"},
            {"name": "key_я", "def": "я", "shift": "Я"},
            {"name": "key_ч", "def": "ч", "shift": "Ч"},
            {"name": "key_с", "def": "с", "shift": "С"},
            {"name": "key_м", "def": "м", "shift": "М"},
            {"name": "key_и", "def": "и", "shift": "И"},
            {"name": "key_т", "def": "т", "shift": "Т"},
            {"name": "key_ь", "def": "ь", "shift": "Ь"},
            {"name": "key_б", "def": "б", "shift": "Б"},
            {"name": "key_ю", "def": "ю", "shift": "Ю"},
            {"name": "key_.", "def": ".", "shift": "."},
            {"name": "key_SHIFT2", "def": "SHIFT", "shift": "SHIFT"},
        ],
        [
            {"name": "key_CTRL1", "def": "CTRL", "shift": "CTRL"},
            {"name": "key_ALT1", "def": "ALT", "shift": "ALT"},
            {"name": "key_SPACE", "def": " ", "shift": " "},
            {"name": "key_ALT1", "def": "ALT", "shift": "ALT"},
            {"name": "key_CTRL2", "def": "CTRL", "shift": "CTRL"},
        ],
    ]

    def __init__(self, lang):
        super().__init__()
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,  # Растягивается по горизонтали
            QtWidgets.QSizePolicy.Policy.Expanding,  # Растягивается по вертикали
        )
        self.vert_layout = QtWidgets.QVBoxLayout(self)
        self.language = lang
        self.keys = self.keys_en if self.language == "english" else self.keys_ru
        for i in range(len(self.keys)):
            keys_layout = QtWidgets.QHBoxLayout()
            keys_layout.setSpacing(5)
            for k in self.keys[i]:
                key = KeyWidget(k['def'])
                print(key.sizePolicy().horizontalPolicy().name)
                key.setObjectName(k['name'])
                if (k['def'] in ['CTRL', 'SHIFT', 'ALT', 'CAPS', 'ENTER', 'TAB']):
                    keys_layout.addWidget(
                        key,  stretch=2
                    )
                elif (k['def'] in [' ', 'BACKSPACE']):
                    keys_layout.addWidget(key, stretch=4)
                # self.key_theme_switch.connect(key.on_theme_switch)
                else:
                    keys_layout.addWidget(
                        key,  stretch=1
                    )
            self.vert_layout.addLayout(
                keys_layout
            )
        # keys_layout = QtWidgets.QHBoxLayout()
        # key = KeyWidget(self.keys[4][0])
        # key.setObjectName("space")
        # self.key_theme_switch.connect(key.on_theme_switch)
        # keys_layout.addWidget(key, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        # self.vert_layout.addLayout(keys_layout)
        # keys = self.central_widget.findChildren(KeyWidget)
        # print(len(keys))
        self.setMinimumSize(500, 300)
        # self.key_lang_change()

    def key_lang_change(self):
        if self.keys == self.keys_en:
            self.keys = self.keys_ru
        else:
            self.keys = self.keys_en

        lts = self.vert_layout.findChildren(QtWidgets.QHBoxLayout)
        for i in range(len(self.keys)):
            for j in range(len(self.keys[i])):
                lts[i].itemAt(j).widget().setText(self.keys[i][j]["def"])
                lts[i].itemAt(j).widget().setObjectName(self.keys[i][j]["name"])

    def on_key_theme_switch(self):
        lts = self.findChildren(QtWidgets.QHBoxLayout)
        for i in range(len(self.keys)):
            for j in range(len(self.keys[i])):
                lts[i].itemAt(j).widget().theme_switch()

    def key_switch(self, name, isPress):
        wid = self.findChild(KeyWidget, name)
        wid.set_active(isPress)
    
    def key_uncorrect(self, name):
        wid = self.findChild(KeyWidget, name)
        wid.set_uncorrect()


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
            f"{self.progress}/{self.total} ({self.progress / self.total:.1%}) | Ошибок: {self.typos}"
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
    key_pressed = QtCore.Signal(str)
    key_released = QtCore.Signal(str)
    textSizeChanged = QtCore.Signal(int)
    typing_start = QtCore.Signal()
    finished = QtCore.Signal()

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
        self.passed_format.setForeground(QtGui.QColor("#ffffff"))

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

    # def setText(self, text):
    #     # self.document().setDefaultStyleSheet(".passed{ color: #f90000; font-size: 25px;}")

    #     self.setHtml(text)

    #     # cursor = self.textCursor()
    #     # cursor.movePosition(QtGui.QTextCursor.MoveOperation.Start)
    #     # # Выделить текущий символ
    #     # cursor.movePosition(QtGui.QTextCursor.MoveOperation.Right, QtGui.QTextCursor.MoveMode.KeepAnchor)
    #     # cursor.mergeCharFormat(self.underline_format)
    #     # cursor.movePosition(QtGui.QTextCursor.MoveOperation.Left)
    #     # self.setTextCursor(cursor)
    #     self.textSizeChanged.emit(len(text))
    #     print(self.textCursor().position(), ' position cursor')

    def setHtmlText(self, text=None):
        if text is None:
            text = self.toPlainText()
            position = self.textCursor().position()
        else:
            position = 0
        htmlText = f"""<span class="passed">{text[:position]}</span><span class="remaining"><span class="current">{text[position:position+1]}</span>{text[position+1:]}</span>"""
        self.setHtml(htmlText)
        cursor = self.textCursor()
        cursor.setPosition(position)
        self.setTextCursor(cursor)


    def get_progress(self):
        print(self.textCursor().position(), " position cursor")
        cursor = self.textCursor()
        return int(cursor.position() / len(self.toPlainText()) * 100)

    def keyName(self, event):
        if event.key() == QtCore.Qt.Key.Key_Space:
            key_name = "key_SPACE"
        elif event.key() == QtCore.Qt.Key.Key_Return:
            key_name = "key_ENTER"
        elif event.key() == QtCore.Qt.Key.Key_Alt:
            key_name = "key_ALT"
        elif event.key() == QtCore.Qt.Key.Key_Shift:
            key_name = "key_SHIFT"
        elif event.key() == QtCore.Qt.Key.Key_Backspace:
            key_name = "key_BACKSPACE"
        elif event.key() == QtCore.Qt.Key.Key_Control:
            key_name = "key_CTRL"
        elif event.key() == QtCore.Qt.Key.Key_CapsLock:
            key_name = "key_CAPS"
        else:
            key_name = "key_" + event.text().lower()
        return key_name

    def keyPressEvent(self, event):
        self.key_pressed.emit(self.keyName(event))

        ch = event.text()
        print(self.textCursor().position(), " position cursor")

        return super().keyPressEvent(event) if event.key() != Qt.Key.Key_Space else None

    def toNextChar(self):
        cursor = self.textCursor()
        if cursor.position() == 0:
            self.typing_start.emit()

        print(cursor.position(), "pos")

        print("perfect")

        cursor.movePosition(
            QtGui.QTextCursor.MoveOperation.Right
        )
        self.setTextCursor(cursor)
        self.setHtmlText()
        # cursor.movePosition(
        #     QtGui.QTextCursor.MoveOperation.Right,
        #     QtGui.QTextCursor.MoveMode.KeepAnchor,
        # )
        # cursor.setCharFormat(self.passed_format)
        # cursor.movePosition(QtGui.QTextCursor.MoveOperation.Left)
        # if len(self.toPlainText()) - 1 == cursor.position():
        #     self.finished.emit()
        # else:
        #     cursor.movePosition(QtGui.QTextCursor.MoveOperation.Right)
        #     cursor.movePosition(
        #         QtGui.QTextCursor.MoveOperation.Right,
        #         QtGui.QTextCursor.MoveMode.KeepAnchor,
        #     )
        #     cursor.mergeCharFormat(self.underline_format)
        #     cursor.movePosition(QtGui.QTextCursor.MoveOperation.Left)
        #     self.setTextCursor(cursor)

        # format = cursor.charFormat()
        # format.setUnderlineStyle(QtGui.QTextCharFormat.UnderlineStyle.SingleUnderline)
        # format.setUnderlineColor("#00c455")  # Подсветка фона
        # format.setBackground(QtCore.Qt.yellow)
        # cursor.setCharFormat(format)
        # self.text_display.setTextCursor(cursor)
        # self.text_display.setCursorPosition(self.text_display.cursorPosition() + 1)

    def keyReleaseEvent(self, event):
        print(type(event))
        self.key_released.emit(self.keyName(event))
        ch = event.text()

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
