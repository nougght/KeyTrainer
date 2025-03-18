from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtGui import QIcon
import sys
from control.main_contol import mainControl


print(QStyleFactory.keys())

if __name__ == "__main__":
    app = QApplication()
    app.setStyle("Fusion")

    main_control = mainControl()
    main_control.setting_control.set_def_style(app)
    app.setWindowIcon(main_control.setting_control.get_icon())
    main_control.show_starter_window()
    sys.exit(app.exec())


