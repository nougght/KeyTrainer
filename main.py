from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtCore import Qt
import sys
from control.main_contol import mainControl

# import qdarkstyle

# запуск приложения
if __name__ == "__main__":
    app = QApplication()
    app.setStyle("Fusion")
    QApplication.setStyle("Fusion")
    
    # основной контроллер
    main_control = mainControl()
    main_control.setting_control.set_base_style(app)
    app.setWindowIcon(main_control.setting_control.get_icon())

    # запуск начального окна
    main_control.show_starter_window()
    sys.exit(app.exec())
