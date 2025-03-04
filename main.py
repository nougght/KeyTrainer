from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtGui import QIcon
import sys
import control.data_control  as dt
from control.main_contol import mainControl


print(QStyleFactory.keys())
if __name__ == "__main__":
    app = QApplication()
    app.setStyle("Fusion")

    with open(dt.resource_path("styles/style.qss"), "r") as f:
        app.setStyleSheet(f.read())
    
        app.setWindowIcon(QIcon(dt.resource_path("data/keyIc.ico")))
        
    main_control = mainControl()
    sys.exit(app.exec())


