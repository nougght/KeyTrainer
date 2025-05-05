from PySide6.QtWidgets import QFrame, QPushButton, QLabel, QComboBox, QWidget, QVBoxLayout, QGridLayout, QScrollArea, QSpacerItem, QSizePolicy, QCheckBox
from PySide6.QtCore import Signal, Slot, Qt, QMargins, QPropertyAnimation, Qt
from PySide6.QtGui import QIcon, QAction, QPen, QColor, QPainter


class SettingsWidget(QFrame):
    user_deleted = Signal()
    def __init__(self):
        super().__init__()
        self.main_layout = QGridLayout(self)
        
        self.username_change_label = QLabel('Сменить имя пользователя')
        self.main_layout.addWidget(self.username_change_label, 0, 0)
        self.password_change_label = QLabel('Сменить пароль')
        self.main_layout.addWidget(self.password_change_label, 1, 0)
        self.username_change_label = QLabel('Сбросить статистику профиля')
        self.main_layout.addWidget(self.username_change_label, 2, 0)

        self.delete_user = QPushButton('Удалить аккаунт')
        self.delete_user.setObjectName('delete_btn')
        self.main_layout.addWidget(self.delete_user, 3, 0, 1, 2)


        spacer1 = QSpacerItem(
            20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.main_layout.addItem(spacer1, 4, 0, 1, 2)
        self.language_change_label = QLabel('Язык интерфейса')
        self.main_layout.addWidget(self.language_change_label, 5, 0)


        
        self.keyboard_visible = QCheckBox('Отображать клавиатуру во время тренировки')
        self.main_layout.addWidget(self.keyboard_visible, 6, 0)




        spacer2 = QSpacerItem(
            20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.main_layout.addItem(spacer2, 7, 0, 1, 2)


        

        self.profile_import_label = QLabel('Импорт аккаунта')
        self.main_layout.addWidget(self.profile_import_label, 8, 0)


        self.profile_export_label = QLabel('Импорт аккаунта')
        self.main_layout.addWidget(self.profile_export_label, 9, 0)
