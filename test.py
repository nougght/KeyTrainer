import sys
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import (QApplication, QMainWindow, QTextEdit, 
                              QVBoxLayout, QWidget, QLabel)
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor, QColor
from ui.other_widgets import KeyWidget

class TypingTutor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Тренажер печати")
        self.setGeometry(100, 100, 800, 400)

        # Текст для тренировки
        self.practice_text = "В чащах юга жил бы цитрус? Да, но фальшивый экземпляр!"
        self.current_pos = 0

        self.init_ui()
        self.update_display()

    def init_ui(self):
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Инструкция
        instruction = QLabel("Начинайте печатать. Текущий символ выделен красным.")
        layout.addWidget(instruction)

        # Текстовое поле для отображения текста
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setStyleSheet("""
            QTextEdit {
                font-family: 'Courier New';
                font-size: 18px;
                background-color: #f8f9fa;
                padding: 15px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.text_display)

        list_widget = QtWidgets.QListWidget()
        list_widget.setFlow(list_widget.Flow.LeftToRight)
        list_widget.setWrapping(True)
        list_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        list_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        list_widget.setSizeAdjustPolicy(QtWidgets.QListWidget.SizeAdjustPolicy.AdjustToContents)
        list_widget.addItems(["Easy", "Normal", "Hard"])
        list_widget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        list_widget.adjustSize()
        list_widget.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        list_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        layout.addWidget(list_widget)

        # Статус
        self.status_label = QLabel()
        layout.addWidget(self.status_label)
    def update_display(self):
        # Формируем HTML с разными классами для частей текста
        html = f"""
        <style>
            .typed {{ color: ; }}
            .current {{ color: #dc3545; font-weight: bold; text-decoration: underline; }}
            .remaining {{ color: #212529; }}
        </style>
        <div class="text-content">
            <span class="typed">{self.practice_text[:self.current_pos]}</span>
            <span class="current">{self.practice_text[self.current_pos] if self.current_pos < len(self.practice_text) else ''}</span>
            <span class="remaining">{self.practice_text[self.current_pos+1:] if self.current_pos+1 < len(self.practice_text) else ''}</span>
        </div>
        """

        self.text_display.setHtml(html)
        self.update_status()

    def update_status(self):
        total = len(self.practice_text)
        typed = self.current_pos
        percent = (typed / total) * 100 if total > 0 else 0

        self.status_label.setText(
            f"Прогресс: {typed}/{total} символов ({percent:.1f}%) | "
            f"Осталось: {total - typed}"
        )

    def keyPressEvent(self, event):
        if event.key() >= Qt.Key_Space and event.key() <= Qt.Key_AsciiTilde:
            char = event.text()
            if self.current_pos < len(self.practice_text):
                if char == self.practice_text[self.current_pos]:
                    self.current_pos += 1
                    self.update_display()
                else:
                    # Можно добавить обработку ошибок
                    pass
        elif event.key() == Qt.Key_Backspace:
            if self.current_pos > 0:
                self.current_pos -= 1
                self.update_display()

        super().keyPressEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TypingTutor()
    window.show()
    sys.exit(app.exec())
