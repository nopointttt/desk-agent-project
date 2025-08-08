# Файл: desk_agent/desk_agent/main.py
import sys
from PyQt6.QtWidgets import QApplication
# ИЗМЕНЕНИЕ: Добавлена точка для явного относительного импорта
from .main_window import MainWindow

def main():
    """
    Основная функция для инициализации и запуска приложения.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()