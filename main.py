from PySide6.QtWidgets import QApplication, QStyleFactory, QDialog
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from my_widgets import StarterDialog
from main_win import MainWindow
import sys, os


def resource_path(relative_path):
    """Get the absolute path to the resource, works for dev and for PyInstaller"""
    if hasattr(sys, "_MEIPASS"):
        # Если приложение запущено из собранного exe
        base_path = sys._MEIPASS
    else:
        # Если приложение запущено из исходного кода
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

print(QStyleFactory.keys())
if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Fusion")

    login_dialog = StarterDialog()
    if login_dialog.exec() == QDialog.Accepted:
        widget = MainWindow()
        widget.showMaximized()
        app.setWindowIcon(QIcon(resource_path("resources/keyIc.ico")))
        with open(resource_path("style.qss"), "r") as f:
            app.setStyleSheet(f.read())
        widget.text_display.setFocus()
        sys.exit(app.exec()) 
