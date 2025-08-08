# ИЗМЕНЕНИЕ: Импортируем конкретные имена
from .constants import TEXT_FRAME, WEB_FRAME
from .frames.base_frame import BaseFrame
from .frames.text_frame import TextFrame
from .frames.web_frame import WebFrame

class FrameFactory:
    def __init__(self):
        self.frame_map = {
            TEXT_FRAME: TextFrame,   # <-- ИЗМЕНЕНИЕ
            WEB_FRAME: WebFrame,   # <-- ИЗМЕНЕНИЕ
        }
        print("[Factory] Фабрика фреймов инициализирована.")

    def create_frame(self, frame_type: str, params: dict) -> BaseFrame | None:
        frame_class = self.frame_map.get(frame_type)
        if frame_class:
            print(f"[Factory] Создание фрейма типа '{frame_type}' с параметрами: {params}")
            return frame_class(**params)
        else:
            print(f"[Factory] Ошибка: неизвестный тип фрейма '{frame_type}'")
            return None