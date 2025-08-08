# Файл: desk_agent/desk_agent/frames/text_frame.py

from PyQt6.QtWidgets import QTextEdit, QFrame
from .base_frame import BaseFrame

class TextFrame(BaseFrame):
    """
    Фрейм, содержащий многострочное текстовое поле для заметок.
    """
    def __init__(self, title="Текстовая заметка", content="", parent=None):
        # 1. Вызываем конструктор родительского класса BaseFrame, передавая ему заголовок.
        # Это создаст рамку, заголовок и всю базовую структуру.
        super().__init__(title, parent)

        # 2. Создаем виджет текстового редактора.
        self.text_edit = QTextEdit()
        
        # 3. Убираем рамку у самого QTextEdit, чтобы не было двойного обрамления.
        # Наш BaseFrame уже предоставляет рамку.
        self.text_edit.setFrameStyle(QFrame.Shape.NoFrame)
        self.text_edit.setPlaceholderText("Введите ваш текст здесь...")
        
        # Если при создании был передан контент, устанавливаем его.
        if content:
            self.text_edit.setText(content)

        # 4. Добавляем созданный текстовый редактор в `content_layout` родительского класса.
        # Этот layout был специально заготовлен в BaseFrame для этой цели.
        self.content_layout.addWidget(self.text_edit)

        # Устанавливаем разумный начальный размер для текстового фрейма.
        self.resize(300, 200)