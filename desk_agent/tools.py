# Файл: desk_agent/desk_agent/tools.py
from time import time
import os
from pathlib import Path

# --- Зона безопасности: Определяем корневую папку для всех файловых операций ---
WORKSPACE_PATH = Path(os.getcwd()) / "workspace"
WORKSPACE_PATH.mkdir(exist_ok=True) # Создаем папку, если ее нет

def _sanitize_path(filepath: str) -> Path | None:
    """Проверяет, что путь находится внутри WORKSPACE_PATH."""
    # Нормализуем путь (убираем '..' и т.д.)
    absolute_path = (WORKSPACE_PATH / filepath).resolve()
    # Проверяем, что разрешенный путь все еще находится внутри нашей рабочей папки
    if WORKSPACE_PATH in absolute_path.parents or absolute_path == WORKSPACE_PATH:
         return absolute_path
    print(f"[SECURITY] Попытка доступа за пределы workspace: {absolute_path}")
    return None

# --- Определения Инструментов ---

def create_text_frame(title: str, content: str = "", x: int = 10, y: int = 10) -> dict:
    """Готовит данные для создания TextFrame. Это основной инструмент вывода информации."""
    return {
        "type": "text_frame",
        "params": {"title": title, "content": content},
        "position": {"x": x, "y": y, "z": time()}
    }

def create_web_frame(url: str, title: str = "Веб-страница", x: int = 50, y: int = 50) -> dict:
    """Готовит данные для создания WebFrame."""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return {
        "type": "web_frame",
        "params": {"title": title, "url": url},
        "position": {"x": x, "y": y, "z": time()}
    }

def list_files(path: str = ".") -> dict:
    """Читает список файлов и папок в директории внутри workspace и выводит его в новый текстовый фрейм."""
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
    """Читает содержимое файла из workspace и выводит его в новый текстовый фрейм."""
    safe_path = _sanitize_path(filepath)
    if not safe_path or not safe_path.is_file():
        return create_text_frame(title="Ошибка доступа", content=f"Файл не найден или доступ запрещен: {filepath}")

    try:
        with open(safe_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return create_text_frame(title=safe_path.name, content=content)
    except Exception as e:
        return create_text_frame(title="Ошибка чтения файла", content=str(e))

def write_to_file(filepath: str, content: str) -> None:
    """Записывает (создает или перезаписывает) текст в файл внутри workspace."""
    safe_path = _sanitize_path(filepath)
    if not safe_path:
        print(f"Отказано в записи в файл: {filepath}")
        return

    try:
        with open(safe_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Успешно записано в файл: {safe_path}")
    except Exception as e:
        print(f"Ошибка записи в файл: {e}")

# --- Реестр Инструментов для LLM ---

TOOLS = [
    # Существующие инструменты
    {
        "name": "create_text_frame",
        "function": create_text_frame,
        "description": "Создает новый текстовый блок или заметку. Используй, если нужно что-то записать по команде пользователя.",
        "parameters": [
            {"name": "title", "type": "string", "description": "Заголовок для текстового блока."},
            {"name": "content", "type": "string", "description": "Текстовое содержимое заметки."}
        ]
    },
    {
        "name": "create_web_frame",
        "function": create_web_frame,
        "description": "Создает окно с веб-браузером и открывает в нем указанный URL. Используй, если пользователь просит открыть сайт или перейти по ссылке.",
        "parameters": [
            {"name": "url", "type": "string", "description": "URL-адрес веб-страницы."},
            {"name": "title", "type": "string", "description": "Опциональный заголовок для окна."}
        ]
    },
    # НОВЫЕ ИНСТРУМЕНТЫ
    {
        "name": "list_files",
        "function": list_files,
        "description": "Показывает список файлов и папок в указанной директории внутри рабочего пространства. Используй, если пользователь спрашивает 'что в этой папке?', 'покажи файлы'.",
        "parameters": [
            {"name": "path", "type": "string", "description": "Путь к директории относительно рабочего пространства. '.' означает текущую директорию."}
        ]
    },
    {
        "name": "read_file",
        "function": read_file,
        "description": "Читает текстовый файл из рабочего пространства и отображает его содержимое. Используй, если пользователь просит 'открой файл', 'прочитай содержимое', 'что в файле'.",
        "parameters": [
            {"name": "filepath", "type": "string", "description": "Путь к файлу внутри рабочего пространства."}
        ]
    },
    {
        "name": "write_to_file",
        "function": write_to_file,
        "description": "Записывает или создает новый текстовый файл в рабочем пространстве с заданным содержимым. Используй, если пользователь просит 'сохрани текст в файл', 'запиши это в файл'. Этот инструмент не создает видимого окна.",
        "parameters": [
            {"name": "filepath", "type": "string", "description": "Имя файла (например, 'report.txt')."},
            {"name": "content", "type": "string", "description": "Текст, который нужно записать в файл."}
        ]
    }
]