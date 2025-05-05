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