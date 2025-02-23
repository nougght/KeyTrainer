from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
class TypingControl(QObject):
    text_changed = Signal(str)
    def __init__(self, text_list_model, word_list_model, main_window):
        super().__init__()
        self.text_list_model = text_list_model
        self.text_list_model.load_from_json("data/texts.json")
        self.word_list_model = word_list_model
        self.word_list_model.load_from_json("data/words.json")

        self.mod = 'words'
        self.difficulty = 'easy'
        self.language = 'english'
        main_window.mod_change.connect(self.on_mod_change)
        main_window.difficulty_change.connect(self.on_difficulty_change)
        self.text_changed.connect(main_window.text_display.setText)
        main_window.on_mid_released()

    def on_mod_change(self, mod="words"):
        self.mod = mod
        if mod == "text":
            text = self.text_list_model.get_random_text(self.language, self.difficulty)
        else:
            length = 20 if self.difficulty == 'easy' else 40 if self.difficulty == 'normal' else 60
            text = self.word_list_model.gen_text(self.language, length)
        self.text_changed.emit(text)


    def on_difficulty_change(self, difficulty="easy"):
        self.difficulty = difficulty
        if self.mod == "text":
            text = self.text_list_model.get_random_text(self.language, difficulty)
        else:
            length = 20 if self.difficulty == 'easy' else 40 if self.difficulty == 'normal' else 60
            text = self.word_list_model.gen_text(self.language, length)
        self.text_changed.emit(text)