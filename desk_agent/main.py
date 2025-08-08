import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow

def main():
    """
    Основная функция для инициализации и запуска приложения.
    """
    # 1. Создание экземпляра QApplication. Требуется для любого приложения PyQt.
    # sys.argv позволяет передавать аргументы командной строки в приложение.
    app = QApplication(sys.argv)

    # 2. Создание и отображение главного окна.
    window = MainWindow()
    window.show()

    # 3. Запуск главного цикла обработки событий приложения.
    # sys.exit() обеспечивает чистое завершение работы.
    sys.exit(app.exec())

if __name__ == '__main__':
    main()