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

# with open(resource_path("styles/light.qss"), "r") as f:
#     light_stylesheet = f.read()
# with open(resource_path("styles/dark.qss"), "r") as f:
#     dark_stylesheet = f.read()



def switch_theme():
    global theme
    theme = "Light" if theme == "Dark" else "Dark"
    with open(resource_path("theme.txt"), "w") as f:
        f.write(theme)
    print(theme)

class KeyTrainerData:
    def __init__(self):
        self.keys_en = [
            ["~","1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "+", "backspace"],
            ["tab", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\"],
            ["caps","a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'", "enter"],
            ["shift","z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "shift"],
            [" "]
        ]
