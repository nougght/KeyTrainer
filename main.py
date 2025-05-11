from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtCore import Qt, QTranslator, QEvent, QFile
from PySide6.QtGui import QIcon
import sys
from control.main_contol import mainControl
import res

# import qdarkstyle


def change_translator(app, translators, language):
    for translator in translators.values():
        app.instance().removeTranslator(translator)

    # Устанавливаем новый, если существует
    if language in translators:
        translator = translators[language]
        if translator.load(f":{language}.qm"):  # Проверяем загрузку
            app.instance().installTranslator(translator)

    # Форсируем обновление интерфейса
    QApplication.instance().sendEvent(
        QApplication.instance(),
        QEvent(QEvent.Type.LanguageChange)
    )


# запуск приложения
if __name__ == "__main__":

    app = QApplication()
    app.setStyle("Fusion")
    QApplication.setStyle("Fusion")

    translators = {
        'ru': QTranslator(),
        'en': QTranslator()
    }
    translators['ru'].load('ru.qm')
    translators['en'].load('en.qm')

    # основной контроллер
    main_control = mainControl()
    main_control.setting_control.set_base_style(app)
    main_control.setting_control.language_changed.connect(lambda tr: change_translator(app, translators, tr))

    app.installTranslator(translators[main_control.setting_control.model.get_language()])

    app.setWindowIcon(QIcon(':/data/keyIc.ico'))

    # запуск начального окна
    main_control.show_starter_window()
    sys.exit(app.exec())
