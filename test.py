from PySide6 import QtWidgets, QtCore


class KeyWidget(QtWidgets.QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,  # Растягивается по горизонтали
            QtWidgets.QSizePolicy.Expanding,  # Растягивается по вертикали
        )
        self.setMinimumSize(50, 50)  # Минимальный размер клавиши


class KeyboardWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # Убедимся, что родительский виджет растягивается
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,  # Растягивается по горизонтали
            QtWidgets.QSizePolicy.Expanding,  # Растягивается по вертикали
        )

        # Основной макет
        self.vert_layout = QtWidgets.QVBoxLayout(self)
        self.vert_layout.setSpacing(5)  # Отступы между строками клавиш

        # Пример раскладки клавиатуры
        self.keys = [
            [
                {"def": "1", "name": "1"},
                {"def": "2", "name": "2"},
                {"def": "3", "name": "3"},
            ],
            [
                {"def": "SHIFT", "name": "Shift"},
                {"def": " ", "name": "Space"},
                {"def": "ALT", "name": "Alt"},
            ],
        ]

        for i in range(len(self.keys)):
            keys_layout = QtWidgets.QHBoxLayout()
            keys_layout.setSpacing(5)  # Отступы между клавишами

            for k in self.keys[i]:
                key = KeyWidget(k["def"])
                key.setObjectName(k["name"])

                # Устанавливаем пропорции для специальных клавиш
                if k["def"] in ["SHIFT", "ALT", " "]:
                    keys_layout.addWidget(
                        key, stretch=3
                    )  # Специальные клавиши занимают больше места
                else:
                    keys_layout.addWidget(
                        key, stretch=1
                    )  # Обычные клавиши занимают меньше места

            self.vert_layout.addLayout(keys_layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    # Главное окно
    window = QtWidgets.QWidget()
    window.setWindowTitle("Keyboard Example")
    window.setGeometry(100, 100, 800, 300)

    # Убедимся, что главное окно растягивается
    window.setSizePolicy(
        QtWidgets.QSizePolicy.Expanding,  # Растягивается по горизонтали
        QtWidgets.QSizePolicy.Expanding,  # Растягивается по вертикали
    )

    # Добавляем клавиатуру в главное окно
    keyboard = KeyboardWidget()
    layout = QtWidgets.QVBoxLayout(window)
    layout.addWidget(keyboard)

    window.show()
    app.exec()
