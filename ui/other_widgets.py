from PySide6.QtWidgets import QTabBar,  QLabel, QFrame,  QTextEdit, QPushButton, QRadioButton, QButtonGroup, QHBoxLayout
from PySide6.QtWidgets import (
    QToolButton,
    QHBoxLayout,
    QMenu,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QLabel,
    QLineEdit
)
from PySide6.QtCore import Signal, Slot, Qt
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6 import QtCore, QtGui, QtWidgets
# from control.settings_control import SettingControl
# import time, os, sys
from html import escape
from utils import resource_path

# различные небольшие виджеты

class LoginInput(QLineEdit):
    def __init__(self, parent=None, placeholderText=None):
        super().__init__(parent, placeholderText=placeholderText)
        self.used_names = None
        self.textChanged.connect(self.check_login)
        self.is_correct = False
        self.warning = self.tr("Логин не может быть пустым")
        self.used_names = []

    def set_used_names(self, names):
        self.used_names = names

    def check_login(self, login):
        import string
        k = [(c in string.ascii_letters.__str__()) for c in login]
        if not login:
            self.warning = self.tr("Логин не может быть пустым")
        elif len(login) < 3:
            self.warning = self.tr("Логин слишком короткий")
        elif not all((c in string.ascii_letters + string.digits + '_') for c in login):
            self.warning = self.tr("Логин должен содержать только символы латинского алфавита, цифры и _")
        elif login in self.used_names:
            self.warning = self.tr("Пользователь с таким именем уже существует")
        else:
            self.warning = None
        self.is_correct = self.warning is None

    def event(self, event):
        from PySide6.QtCore import QEvent

        if event.type() == QEvent.Type.LanguageChange:
            self.retranslate()
        return super().event(event)

    def retranslate(self):
        self.check_login(self.text())


class PasswordInput(QLineEdit):
    def __init__(self, parent=None, placeholderText=None):
        super().__init__(parent, placeholderText=placeholderText)
        self.echo_mode_btn = QAction()
        self.addAction(self.echo_mode_btn, QLineEdit.ActionPosition.TrailingPosition)
        # self.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Z]+")))
        self.echo_mode_btn.triggered.connect(self.switch_echo_mode)
        self.echo_icon_path = "assets/weye.svg"
        self.echo_icon_slash_path = "assets/weye-slash.svg"
        self.switch_echo_mode()
        self.textChanged.connect(self.check_password)
        self.is_correct = False
        self.warning = self.tr("Пароль не может быть пустым")

    # def switch_correct_icon(self):
    #     if self.is_correct is True:
    #         self.correct_icon.setIcon(QIcon(resource_path("assets/checkmark.svg")))
    #     else:
    #         self.correct_icon.setIcon(QIcon(resource_path("assets/cross.svg")))

    def switch_echo_mode(self):
        if self.echoMode() == QLineEdit.EchoMode.Password:
            self.setEchoMode(QLineEdit.EchoMode.Normal)
            self.echo_mode_btn.setIcon(QIcon(f':/{self.echo_icon_slash_path}'))
        else:
            self.setEchoMode(QLineEdit.EchoMode.Password)
            self.echo_mode_btn.setIcon(QIcon(f":/{self.echo_icon_path}"))

    def switch_icon_theme(self, theme):
        if theme == 'defaultDark':
            self.echo_icon_path = 'assets/weye.svg'
            self.echo_icon_slash_path = "assets/weye-slash.svg"
        else:
            self.echo_icon_path = "assets/beye.svg"
            self.echo_icon_slash_path = "assets/beye-slash.svg"

        if self.echoMode() == QLineEdit.EchoMode.Password:
            self.echo_mode_btn.setIcon(QIcon(f":/{self.echo_icon_path}"))
        else:
            self.echo_mode_btn.setIcon(QIcon(f":/{self.echo_icon_slash_path}"))

    def check_password(self, password):
        import string
        if len(password) < 8:
            self.warning = self.tr("Пароль слишком короткий")
        elif not all((c in string.ascii_letters + string.digits) for c in password):
            self.warning = self.tr("Допустимы только буквы латинского алфавита и цифры")
        elif not any(c.isdigit() for c in password):
            self.warning = self.tr("Добавьте хотя бы одну цифру")
        elif not any((c in string.ascii_letters) for c in password):
            self.warning = self.tr("Добавьте хотя бы одну букву")
        else:
            self.warning = None
        self.is_correct = self.warning is None
        # self.switch_correct_icon()

    def event(self, event):
        from PySide6.QtCore import QEvent

        if event.type() == QEvent.Type.LanguageChange:
            self.retranslate()
        return super().event(event)

    def retranslate(self):
        self.check_password(self.text())


class TabBarWithControl(QFrame):
    CloseClicked = Signal()
    MinimiseClicked = Signal()
    TabChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        # self.setStyleSheet('border-bottom: 1px solid #2b2e4a;background: #3a11cd;')
        self.setObjectName("TabPanel")
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.tabBar = QTabBar()
        self.tabBar.setDrawBase(False)
        # self.tabBar.setStyleSheet('background: red;')
        layout.addWidget(self.tabBar, alignment=Qt.AlignmentFlag.AlignBottom)

        spacer = QSpacerItem(
            20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        layout.addItem(spacer)

        self.right_widget = QFrame(self)
        self.right_widget.setObjectName("Corner")
        self.right_widget.setLayout(QHBoxLayout(self.right_widget))
        self.right_widget.layout().setContentsMargins(0, 0, 0, 0)
        self.right_widget.layout().setSpacing(0)
        self.theme_button = ThemeButton()
        self.minimise_btn = QPushButton("—", self)
        self.minimise_btn.setObjectName("minimiseButton")
        self.minimise_btn.clicked.connect(self.MinimiseClicked.emit)
        self.close_btn = QPushButton("✕", self)
        self.close_btn.setObjectName("exitButton")
        self.close_btn.clicked.connect(self.CloseClicked.emit)
        self.right_widget.layout().addWidget(self.theme_button)
        self.right_widget.layout().addWidget(self.minimise_btn)
        self.right_widget.layout().addWidget(self.close_btn)
        layout.addWidget(self.right_widget)


class ThemeButton(QToolButton):
    theme_changed = Signal(str)  # Сигнал при смене темы

    def __init__(self):
        super().__init__()
        # self.setText("🎨")
        # self.setIcon(QIcon(resource_path("assets/themes.svg")))  # Иконка смены темы
        self.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)  # Меню по клику
        self._setup_menu()

    def _setup_menu(self):
        self._menu = QMenu(self)
        themes = ["defaultDark", "defaultLight"]
        for theme in themes:
            action = self._menu.addAction(theme)
            # action.triggered.connect(lambda: self.theme_changed.emit(theme))
        self._menu.triggered.connect(lambda action: self.theme_changed.emit(action.text()))
        self.setMenu(self._menu)


class KeyWidget(QPushButton):
    styles = ["background: #88C0D0; color: #090f1b; border: 2px solid #090f1b;",
             "background: #090f1b; border: 2px solid #88C0D0; color: #88C0D0;"]

    def __init__(self, text, parent=None, isdark=False):
        super().__init__(text, parent)
        self.setMinimumSize(60, 60)  # Минимальный размер клавиши
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,  # Растягивается по горизонтали
            QtWidgets.QSizePolicy.Policy.Fixed,  # Растягивается по вертикали
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


class KeyboardWidget(QtWidgets.QFrame):
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
            {"name": "key_BACKSPACE", "def": "BACK", "shift": "BACKSPACE"},
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
            {"name": "key_SHIFT1", "def": "SHIFT", "shift": "SHIFT"},
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
            {"name": "key_SHIFT2", "def": "SHIFT", "shift": "SHIFT"},
        ],
        [
            {"name": "key_CTRL1", "def": "CTRL", "shift": "CTRL"},
            {"name": "key_ALT", "def": "ALT", "shift": "ALT"},
            {"name": "key_SPACE", "def": " ", "shift": " "},
            {"name": "key_ALT", "def": "ALT", "shift": "ALT"},
            {"name": "key_CTRL2", "def": "CTRL", "shift": "CTRL"},
        ],
    ]
    keys_ru = [
        [
            {"name": "key_ё", "def": "ё", "shift": "Ё"},
            {"name": "key_1", "def": "1", "shift": "!"},
            {"name": "key_2", "def": "2", "shift": "\""},
            {"name": "key_3", "def": "3", "shift": "№"},
            {"name": "key_4", "def": "4", "shift": ";"},
            {"name": "key_5", "def": "5", "shift": "%"},
            {"name": "key_6", "def": "6", "shift": ":"},
            {"name": "key_7", "def": "7", "shift": "?"},
            {"name": "key_8", "def": "8", "shift": "*"},
            {"name": "key_9", "def": "9", "shift": "("},
            {"name": "key_0", "def": "0", "shift": ")"},
            {"name": "key_-", "def": "-", "shift": "_"},
            {"name": "key_+", "def": "+", "shift": "+"},
            {"name": "key_BACKSPACE", "def": "BACK", "shift": "BACKSPACE"},
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
            {"name": "key_\\", "def": "\\", "shift": "/"},
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
            {"name": "key_.", "def": ".", "shift": ","},
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
        self.vert_layout.setContentsMargins(0, 0, 0, 0)
        self.language = lang
        self.keys = self.keys_en if self.language == "english" else self.keys_ru

        for i in range(len(self.keys)):
            keys_layout = QtWidgets.QHBoxLayout()
            keys_layout.setSpacing(2)
            for k in self.keys[i]:
                key = KeyWidget(k['def'])
                #print(key.sizePolicy().horizontalPolicy().name)
                key.setObjectName(k['name'])
                if (k['def'] in ['CTRL', 'SHIFT', 'ALT', 'CAPS', 'ENTER', 'TAB','BACKSPACE']):

                    key.setSizePolicy(
                        QtWidgets.QSizePolicy.Policy.Expanding,  # Растягивается по горизонтали
                        QtWidgets.QSizePolicy.Policy.Expanding,  # Растягивается по вертикали
                    )
                    keys_layout.addWidget(
                        key,  stretch=2
                    )
                elif (k['def'] in [' ', ]):
                    keys_layout.addWidget(key, stretch=4)
                    key.setSizePolicy(
                        QtWidgets.QSizePolicy.Policy.Expanding,  # Растягивается по горизонтали
                        QtWidgets.QSizePolicy.Policy.Expanding,  # Растягивается по вертикали
                    )
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
        # #print(len(keys))
        self.setMinimumSize(500, 300)
        # self.key_lang_change()

    def key_lang_change(self, lang):
        if lang == 'russian':
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
        if wid is None:
            self.findChild(KeyWidget, "key_SHIFT1").set_active(isPress)
        else:
            wid.set_active(isPress)
    def key_uncorrect(self, name):
        wid = self.findChild(KeyWidget, name)
        if wid is not None:
            wid.set_uncorrect()


class KeyProgressDisplay(QLabel):
    def __init__(self, total = 0):
        self.total = total
        self.progress = 0
        self.typos = 0
        self.er_mes = self.tr('Ошибок')
        super().__init__(self.get_text())

    def get_text(self):
        return f"{self.progress}/{self.total} ({self.progress / self.total:.1%})\t {self.er_mes}: {self.typos}"
    
    def reset(self, new_total = 0):
        self.total = new_total
        self.progress = 0
        self.typos = 0
        self.setText(
            f"{self.progress}/{self.total} ({self.progress / self.total:.1%})\t {self.er_mes}: {self.typos}"
        )

    @QtCore.Slot()
    def on_inc_progress(self):
        self.progress += 1
        self.setText(
            f"{self.progress}/{self.total} ({self.progress / self.total:.1%})\t {self.er_mes}: {self.typos}"
        )

    @QtCore.Slot()
    def on_typo(self):
        self.typos += 1
        self.setText(
            f"{self.progress}/{self.total} ({self.progress / self.total:.1%})\t {self.er_mes}: {self.typos}"
        )

class RadioList(QFrame):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(10) 
        self.layout.setContentsMargins(0, 0, 0, 0) 
        
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)  # Включаем режим "только один выбор"

        

    def add_items(self, items):
        for i, text in enumerate(items):
            btn = QRadioButton(text)
            self.button_group.addButton(btn, i)
            self.layout.addWidget(btn)

        # Делаем первую кнопку выбранной по умолчанию
        if items:
            self.button_group.button(0).setChecked(True)

class KeyTextEdit(QTextEdit):
    key_pressed = QtCore.Signal(str, bool)
    key_released = QtCore.Signal(str)
    textSizeChanged = QtCore.Signal(int)
    typing_start = QtCore.Signal()
    finished = QtCore.Signal()

    def __init__(self):
        super().__init__()
        # Инициализация формата подчёркивания
        self.text = ''
        self.underline_format = QtGui.QTextCharFormat()
        self.underline_format.setUnderlineStyle(
            QtGui.QTextCharFormat.UnderlineStyle.SingleUnderline
        )
        self.underline_format.setUnderlineColor(QtGui.QColor("#9480eb"))

        self.passed_format = QtGui.QTextCharFormat()
        self.passed_format.setBackground(QtGui.QColor("#279346"))
        self.passed_format.setForeground(QtGui.QColor("#ffffff"))

        self.setReadOnly(True)

        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        # self.text_display.setFixedHeight(150)
        # self.setFixedHeight(200)
        self.setFont(QtGui.QFont("Consolas", 50, 500))
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
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
    #     #print(self.textCursor().position(), ' position cursor')


    def adjust_position(self, original_text, position):
        escaped_part = escape(original_text[:position])
        return len(escaped_part)  # Новая позиция в экранированном тексте
    
    def setHtmlText(self, text=None):
        if text is None:
            text = self.text
            original_position = self.textCursor().position()
            position = original_position # Пересчитываем позицию
        else:
            self.text = text
            position = 0
        
        
        passed = escape(text[:position])
        current = escape(text[position:position+1])
        remaining = escape(text[position+1:])

        # text = text[:position+1] + escape(text[position+1:])
        htmlText = f"""<span class="passed">{passed}</span><span class="remaining"><span class="current">{current}</span>{remaining}</span>"""
        self.setHtml(htmlText)
        cursor = self.textCursor()
        cursor.setPosition(position)
        self.setTextCursor(cursor)

    def get_progress(self):
        #print(self.textCursor().position(), " position cursor")
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
            key_name = "key_SHIFT1"
        elif event.key() == QtCore.Qt.Key.Key_Backspace:
            key_name = "key_BACKSPACE"
        elif event.key() == QtCore.Qt.Key.Key_Control:
            key_name = "key_CTRL1"
        elif event.key() == QtCore.Qt.Key.Key_CapsLock:
            key_name = "key_CAPS"
        else:
            key_name = "key_" + event.text().lower()
        return key_name

    def keyPressEvent(self, event):

        self.key_pressed.emit(self.keyName(event), event.modifiers() & Qt.KeyboardModifier.ShiftModifier)

        ch = event.text()

        #print(self.textCursor().position(), " position cursor")

        return super().keyPressEvent(event) if event.key() != Qt.Key.Key_Space and event.key() != Qt.Key.Key_Shift else None

    def toNextChar(self):
        cursor = self.textCursor()
        # if cursor.position() == 0:
        #     self.typing_start.emit()

        #print(cursor.position(), "pos")

        #print("perfect")

        cursor.movePosition(
            QtGui.QTextCursor.MoveOperation.Right
        )
        self.setTextCursor(cursor)
        self.setHtmlText()

        cursor_rect = self.cursorRect()
        viewport_height = self.viewport().height()
        margin = cursor_rect.height()  # Пикселей до нижнего края, когда начинаем прокрутку
        
        if cursor_rect.bottom() > viewport_height - margin:
            scrollbar = self.verticalScrollBar()
            scrollbar.setValue(scrollbar.value() + cursor_rect.height())

    def keyReleaseEvent(self, event):
        #print(type(event))
        self.key_released.emit(self.keyName(event))
        ch = event.text()

        return super().keyPressEvent(event) if event.key() != QtCore.Qt.Key.Key_Space else None

    # отключение событий поля
    def mousePressEvent(self, e):
        pass
        # return super().mousePressEvent(e)
    def mouseDoubleClickEvent(self, e):
        pass
        # return super().mouseDoubleClickEvent(e)
    def mouseMoveEvent(self, e):
        pass
        # return super().mouseMoveEvent(e)
