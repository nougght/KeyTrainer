from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

# контроллер настроек
class SettingControl(QtCore.QObject):
    theme_changed = Signal(list)  # сигнал смены стиля
    language_changed = Signal(str)  # сигнал смены языка

    def __init__(self, settings_model, main_window, start_window):
        super().__init__()
        self.model = settings_model
        self.start_window = start_window
        self.main_window = main_window

        main_window.setWindowStyle(self.model.get_theme_style())
        start_window.setStyleSheet(self.model.get_theme_style()[0])
        start_window.login_form.set_last_user(settings_model.get_last_user())
        start_window.change_theme.connect(self.on_theme_change)
        main_window.change_theme.connect(self.on_theme_change)
        self.theme_changed.connect(
            lambda style: main_window.setWindowStyle(style)
        )
        self.theme_changed.connect(lambda style: start_window.setStyleSheet(style[0]))

        start_window.change_language.connect(self.on_language_change)
        main_window.settings_widget.change_language.connect(self.on_language_change)
        start_window.set_lang_combo(self.model.get_language())
        main_window.settings_widget.set_lang_combo(self.model.get_language())
        # self.theme_changed.connect(main_window.typing_widget.on_key_theme_switch)

    def set_user(self, user_id):
        self.model.set_last_user(user_id)

    def on_theme_change(self, theme):
        self.model.switch_theme(theme)
        print(self.model.get_theme())
        self.theme_changed.emit(self.model.get_theme_style())

        # val = 'd' if theme == 'defaultDark' else 'l'
        # self.start_window.style_btn.setProperty('t', val)
        # self.main_window.tab.theme_button.setProperty('t', val)
        self.start_window.login_form.password_input.switch_icon_theme(theme)
        self.start_window.registration_form.password_input.switch_icon_theme(theme)
        self.start_window.registration_form.password_verify_input.switch_icon_theme(theme)
        self.start_window.registration_form.recovery_input.switch_icon_theme(theme)
        self.start_window.recovery_form.new_password_input.switch_icon_theme(theme)
        self.start_window.recovery_form.password_verify_input.switch_icon_theme(theme)
        self.main_window.settings_widget.password_change_form.new_password_input.switch_icon_theme(theme)
        self.main_window.settings_widget.password_change_form.password_input.switch_icon_theme(theme)
        self.main_window.settings_widget.password_change_form.password_verify_input.switch_icon_theme(theme)
    # обработчик смены языка приложения
    def on_language_change(self, language):
        self.model.set_language(language)
        self.start_window.set_lang_combo(self.model.get_language())
        self.main_window.settings_widget.set_lang_combo(self.model.get_language())
        self.language_changed.emit(self.model.get_language())
    # установка базовых стилей
    def set_base_style(self, wid: QWidget):
        wid.setStyleSheet(self.model.get_base_style())
    # установка текущего стиля приложения
    def set_curr_style(self, wid: QWidget):
        wid.setStyleSheet(self.model.get_theme_style()[0])

    # def get_icon(self):
    #     return self.model.icon

    # def set_light_style(self, wid: QWidget):
    #     wid.setStyleSheet(self.model.get_light_style())

    # def set_dark_style(self, wid: QWidget):
    #     wid.setStyleSheet(self.model.get_dark_style())
