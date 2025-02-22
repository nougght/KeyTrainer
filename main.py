from PySide6.QtWidgets import QApplication, QStyleFactory, QDialog
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from ui.my_widgets import StarterDialog
from ui.main_win import MainWindow
import sys
import control.data_control  as dt
from control.main_contol import mainControl


print(QStyleFactory.keys())
if __name__ == "__main__":
    app = QApplication()
    app.setStyle("Fusion")

    with open(dt.resource_path("styles/style.qss"), "r") as f:
        app.setStyleSheet(f.read())
    
        app.setWindowIcon(QIcon(dt.resource_path("resources/keyIc.ico")))
        
    main_control = mainControl()
    sys.exit(app.exec())
    print(1)

