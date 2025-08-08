# Файл: desk_agent/desk_agent/tool_definitions.py

# Импортируем реальные функции из соседнего модуля
from . import tool_functions as tf

# Реестр Инструментов для LLM
TOOLS = [
    {
        "name": "create_text_frame",
        "function": tf.create_text_frame,
        "description": "Создает новый текстовый блок или заметку для записи мыслей, идей или любой текстовой информации. Полезен, когда нужно что-то записать.",
        "parameters": [
            {"name": "title", "type": "string", "description": "Заголовок для текстового блока."},
            {"name": "content", "type": "string", "description": "Основное текстовое содержимое заметки."}
        ]
    },
    {
        "name": "create_web_frame",
        "function": tf.create_web_frame,
        "description": "Создает окно с веб-браузером и открывает в нем указанный URL. Используй, если пользователь просит открыть сайт или перейти по ссылке.",
        "parameters": [
            {"name": "url", "type": "string", "description": "URL-адрес веб-страницы."},
            {"name": "title", "type": "string", "description": "Опциональный заголовок для окна."}
        ]
    },
    {
        "name": "list_files",
        "function": tf.list_files,
        "description": "Показывает список файлов и папок в указанной директории внутри рабочего пространства. Используй, если пользователь спрашивает 'что в этой папке?', 'покажи файлы'.",
        "parameters": [
            {"name": "path", "type": "string", "description": "Путь к директории относительно рабочего пространства. '.' означает текущую директорию."}
        ]
    },
    {
        "name": "read_file",
        "function": tf.read_file,
        "description": "Читает текстовый файл из рабочего пространства и отображает его содержимое. Используй, если пользователь просит 'открой файл', 'прочитай содержимое', 'что в файле'.",
        "parameters": [
            {"name": "filepath", "type": "string", "description": "Путь к файлу внутри рабочего пространства."}
        ]
    },
    {
        "name": "write_to_file",
        "function": tf.write_to_file,
        "description": "Записывает или создает новый текстовый файл в рабочем пространстве с заданным содержимым. Используй, если пользователь просит 'сохрани текст в файл', 'запиши это в файл'. Этот инструмент не создает видимого окна.",
        "parameters": [
            {"name": "filepath", "type": "string", "description": "Имя файла (например, 'report.txt')."},
            {"name": "content", "type": "string", "description": "Текст, который нужно записать в файл."}
        ]
    }
]