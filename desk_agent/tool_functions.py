import os
from time import time
from pathlib import Path
# ИЗМЕНЕНИЕ: Импортируем конкретные имена, а не весь модуль
from .constants import TEXT_FRAME, WEB_FRAME

WORKSPACE_PATH = Path(os.getcwd()) / "workspace"
WORKSPACE_PATH.mkdir(exist_ok=True)

def _sanitize_path(filepath: str) -> Path | None:
    absolute_path = (WORKSPACE_PATH / filepath).resolve()
    if WORKSPACE_PATH in absolute_path.parents or absolute_path == WORKSPACE_PATH:
         return absolute_path
    print(f"[SECURITY] Попытка доступа за пределы workspace: {absolute_path}")
    return None

def create_text_frame(title: str, content: str = "", x: int = 10, y: int = 10) -> dict:
    return {
        "type": TEXT_FRAME, # <-- ИЗМЕНЕНИЕ
        "params": {"title": title, "content": content},
        "position": {"x": x, "y": y, "z": time()}
    }

def create_web_frame(url: str, title: str = "Веб-страница", x: int = 50, y: int = 50) -> dict:
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return {
        "type": WEB_FRAME, # <-- ИЗМЕНЕНИЕ
        "params": {"title": title, "url": url},
        "position": {"x": x, "y": y, "z": time()}
    }

def list_files(path: str = ".") -> dict:
    safe_path = _sanitize_path(path)
    if not safe_path:
        return create_text_frame(title="Ошибка доступа", content=f"Запрещен доступ к пути: {path}")
    try:
        files = os.listdir(safe_path)
        content = "\n".join(files) if files else "Папка пуста."
        return create_text_frame(title=f"Содержимое: {path}", content=content)
    except Exception as e:
        return create_text_frame(title="Ошибка чтения", content=str(e))

def read_file(filepath: str) -> dict:
    safe_path = _sanitize_path(filepath)
    if not safe_path or not safe_path.is_file():
        return create_text_frame(title="Ошибка доступа", content=f"Файл не найден или доступ запрещен: {filepath}")
    try:
        with open(safe_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return create_text_frame(title=safe_path.name, content=content)
    except Exception as e:
        return create_text_frame(title="Ошибка чтения файла", content=str(e))

def write_to_file(filepath: str, content: str) -> str:
    safe_path = _sanitize_path(filepath)
    if not safe_path:
        msg = f"Отказано в записи в файл: {filepath}"
        print(msg)
        return msg
    try:
        with open(safe_path, 'w', encoding='utf-8') as f:
            f.write(content)
        msg = f"Файл '{safe_path.name}' успешно сохранен."
        print(msg)
        return msg
    except Exception as e:
        msg = f"Ошибка записи в файл: {e}"
        print(msg)
        return msg