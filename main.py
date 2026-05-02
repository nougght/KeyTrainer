from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtCore import Qt, QTranslator, QEvent, QFile
from PySide6.QtGui import QIcon
import sys
from control import MainControl
import res  # qrc модуль с ресурсами


# переключатель перевода
def change_translator(app, translators, language):
    for translator in translators.values():
        app.instance().removeTranslator(translator)

    # установка нужного файла из ресурсов
    if language in translators:
        translator = translators[language]
        if translator.load(f":assets/{language}.qm"):  # Проверяем загрузку
            app.instance().installTranslator(translator)

    # обновление интерфейса
    QApplication.instance().sendEvent(
        QApplication.instance(),
        QEvent(QEvent.Type.LanguageChange)
    )

# запуск приложения
def main():
    app = QApplication()
    app.setStyle("Fusion")   
    QApplication.setStyle("Fusion")
    translators = {
        'ru': QTranslator(),
        'en': QTranslator()
    }

    # основной контроллер (отвечает за связывание всех модулей)
    main_control = MainControl()
    main_control.setting_control.set_base_style(app)

    # связываем сигнал изменения языка с функцией
    main_control.setting_control.language_changed.connect(lambda tr: change_translator(app, translators, tr))

    app.setWindowIcon(QIcon(':/assets/keyIc.ico'))
    app.installTranslator(
        translators[main_control.setting_control.model.get_language()]
    )
    change_translator(app, translators, main_control.settings_model.get_language())

    # отображение окна входа
    main_control.show_starter_window()
    # запуск приложения
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
