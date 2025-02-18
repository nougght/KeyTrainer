from PySide6.QtWidgets import QApplication, QStyleFactory, QDialog
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from my_widgets import StarterDialog
from main_win import MainWindow
import sys
import my_data  as dt



print(QStyleFactory.keys())
if __name__ == "__main__":
    app = QApplication()
    app.setStyle("Fusion")

    with open(dt.resource_path("style.qss"), "r") as f:
        app.setStyleSheet(f.read())
    login_dialog = StarterDialog()
    if login_dialog.exec() == QDialog.Accepted:
        widget = MainWindow()
        widget.showFullScreen()
        app.setWindowIcon(QIcon(dt.resource_path("resources/keyIc.ico")))


        widget.text_display.setFocus()
        sys.exit(app.exec()) 
        
