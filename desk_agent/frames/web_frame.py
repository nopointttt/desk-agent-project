# Файл: desk_agent/desk_agent/frames/web_frame.py

from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import QUrl
# Импортируем виджет веб-браузера
from PyQt6.QtWebEngineWidgets import QWebEngineView

from .base_frame import BaseFrame

class WebFrame(BaseFrame):
    """
    Фрейм, содержащий веб-браузер для отображения страниц по URL.
    """
    def __init__(self, title="Веб-страница", url="", parent=None):
        super().__init__(title, parent)

        self.web_view = QWebEngineView()

        # Если URL предоставлен, загружаем его
        if url:
            self.web_view.load(QUrl(url))

        # Добавляем виджет браузера в область контента
        self.content_layout.addWidget(self.web_view)

        # Устанавливаем разумный начальный размер
        self.resize(600, 400)