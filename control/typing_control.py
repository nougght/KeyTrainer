from PySide6.QtCore import QObject, Signal, Qt, QTimer
from model.typing_session import TypingSession
import time, sys, os

class TypingControl(QObject):
    # toolbt_activate = Signal(str, bool)
    keyboard_lang_change = Signal(str)
    typing_stats = Signal(float, float, TypingSession)
    text_changed = Signal(str)
    correctPress = Signal(str)
    toNextChar = Signal(str)
    typo = Signal(str)
    release = Signal(str)
    def __init__(self, text_repository,  main_window):
        super().__init__()
        self.main_window = main_window

        self.is_shift_pressed = False

        self.timer = QTimer(self)
        self.timer.setTimerType(Qt.PreciseTimer)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.on_timer)

        self.session = TypingSession()
        self.text = ''
        self.position = 0
        self.errors = 0

        self.text_repository = text_repository

        # self.toolbt_activate.connect(main_window.typing_widget.toolbutton_activate)
        # self.text_list_model = text_list_model
        # self.text_list_model.load_from_json(self.resource_path("data/texts.json"))
        # self.word_list_model = word_list_model
        # self.word_list_model.load_from_json(self.resource_path("data/words.json"))

        self.mod = 'words'
        self.difficulty = 'easy'
        self.language = "english"
        # self.toolbt_activate.emit(self.mod, True)
        # self.toolbt_activate.emit(self.difficulty, True)
        # self.toolbt_activate.emit(self.language, True)

        # main_window.finish.accepted.connect(self.change_text)
        main_window.typing_widget.reset_button.clicked.connect(self.change_text)
        main_window.typing_widget.language_change.connect(self.on_language_change)
        main_window.typing_widget.mod_change.connect(self.on_mod_change)
        main_window.typing_widget.difficulty_change.connect(self.on_difficulty_change)
        main_window.typing_widget.text_display.typing_start.connect(self.on_typing_start)
        main_window.typing_widget.text_display.key_pressed.connect(self.on_key_press)
        main_window.typing_widget.text_display.key_released.connect(self.on_key_release)
        self.correctPress.connect(main_window.typing_widget.text_display.toNextChar)
        self.correctPress.connect(lambda key: main_window.typing_widget.keyboard_widget.key_switch(key, False))
        self.toNextChar.connect(lambda key: main_window.typing_widget.keyboard_widget.key_switch(key, True))

        self.typo.connect(main_window.typing_widget.keyboard_widget.key_uncorrect)
        self.typo.connect(main_window.typing_widget.char_pos_label.on_typo)

        self.correctPress.connect(
            main_window.typing_widget.char_pos_label.on_inc_progress
        )
        self.text_changed.connect(main_window.typing_widget.text_display.setHtmlText)
        self.text_changed.connect(
            lambda text: main_window.typing_widget.char_pos_label.reset(len(text))
        )
        self.text_changed.connect(
            lambda: main_window.typing_widget.progress_bar.setValue(self.position)
        )
        self.correctPress.connect(
            lambda: main_window.typing_widget.progress_bar.setValue(
                self.position / len(self.text) * 100
            )
        )
        self.release.connect(
            lambda key: main_window.typing_widget.keyboard_widget.key_switch(key, False)
        )
        self.typing_stats.connect(main_window.typing_widget.on_stats_display)
        self.keyboard_lang_change.connect(
            main_window.typing_widget.keyboard_widget.key_lang_change
        )
        self.change_text()

    def on_timer(self):
        print(time.time())
        self.session.on_time()

    def change_text(self):
        if len(self.text) > 0 and self.position < len(self.text):
            self.correctPress.emit("key_" + self.text[self.position].lower())
        if self.mod == "text" and self.language not in ["python", "cpp"]:
            self.text = self.text_repository.get_text(self.language, self.difficulty)
        else:
            length = 15 if self.difficulty == 'easy' else 40 if self.difficulty == 'normal' else 60
            self.text = self.text_repository.get_words(self.language, length)
        self.position = 0
        print(self.text)
        self.text_changed.emit(self.text)
        self.toNextChar.emit("key_" + self.text[self.position].lower())

    def on_key_press(self, key_name, is_shift):
        # key = key_name.split('_')[1]
        key = None
        for row in self.main_window.typing_widget.keyboard_widget.keys:
            for k in row:
                if k["name"] == key_name:
                    key = k
                    break
                elif f'key_{k["shift"]}' == key_name:
                    key = k
                    break
            if key is not None:
                break
        if key:
            if self.is_shift_pressed is True:
                key = key["shift"]
            else:
                key = key['def']
        # key = key['def']

        if self.position == 0:
            self.on_typing_start()
        print(self.position)
        if key and len(key) == 1 and self.text[self.position] == (key.upper() if is_shift else key) or key == 'SPACE' and self.text[self.position] == ' ':
            self.position += 1
            self.session.add_keystroke(key, True)
            self.correctPress.emit(key_name)
            if self.position == len(self.text):
                self.release.emit(key_name)
                self.on_typing_finished()
            nextKey = 'key_' + ('SPACE' if self.text[self.position] == ' ' else self.text[self.position])
            self.toNextChar.emit(nextKey)
        elif key == "SHIFT":
            self.is_shift_pressed = True
        elif key not in ["SHIFT", "CAPS", "ALT"]:
            self.session.add_keystroke(key, False)
            self.typo.emit(key_name)
            self.errors += 1

    def on_key_release(self, key_name):
        key = key_name.split("_")[1]
        if key == "SHIFT1":
            self.is_shift_pressed = False

        self.release.emit(key_name)

    def on_typing_start(self):
        self.session.reset_stats()
        self.start_time = time.time()
        self.timer.start()
        self.session.start_session(f"{self.language}/{self.mod}")
        print(self.start_time)

    def on_typing_finished(self):
        self.timer.stop()
        self.session.finish_session()
        # print(f'----------\n{self.session.stats['duration']}       {self.session.stats['time'][-1]}\n-------------')
        self.finish_time = time.time()
        typing_time = self.finish_time - self.start_time

        self.typing_stats.emit(len(self.text) / typing_time * 60, typing_time, self.session)
        self.session.reset_stats()

    def on_language_change(self, language="english"):
        if self.language != language.lower():
            # self.toolbt_activate.emit(self.language, False)
            self.language = language
            # self.toolbt_activate.emit(language, True)
            self.correctPress.emit("key_" + self.text[self.position].lower())
            self.keyboard_lang_change.emit(language)
            self.change_text()

    def on_mod_change(self, mod="words"):
        if self.mod != mod.lower():
            # self.toolbt_activate.emit(self.mod, False)
            self.mod = mod
            self.change_text()
            # self.toolbt_activate.emit(mod, True)

    def on_difficulty_change(self, difficulty="easy"):
        if self.difficulty != difficulty.lower():
            # self.toolbt_activate.emit(self.difficulty, False)
            self.difficulty = difficulty
            self.change_text()
            # self.toolbt_activate.emit(difficulty, True)

    def resource_path(self, relative_path):
        """Get the absolute path to the resource, works for dev and for PyInstaller"""
        if hasattr(sys, "_MEIPASS"):
            # Если приложение запущено из собранного exe
            base_path = sys._MEIPASS
        else:
            # Если приложение запущено из исходного кода
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
