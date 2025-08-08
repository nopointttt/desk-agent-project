# Файл: desk_agent/desk_agent/main_window.py

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QLineEdit, QPushButton, QDockWidget
)
from PyQt6.QtCore import Qt, QThread, pyqtSlot, QTimer

from custom_scene import GridScene
from custom_view import ZoomableView
from ai_service import AIService
# --- НОВЫЙ ИМПОРТ ---
from frames.text_frame import TextFrame
from frames.web_frame import WebFrame

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DESK Агент")
        self.setGeometry(100, 100, 1280, 720)

        self.scene = GridScene()
        self.graphics_view = ZoomableView(self.scene)
        self.setCentralWidget(self.graphics_view)

        self.setup_command_interface()
        self.setup_ai_service()

    def setup_command_interface(self):
        # ... (без изменений)
        self.command_dock = QDockWidget("Управление Агентом", self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.command_dock)
        dock_content = QWidget()
        dock_layout = QVBoxLayout(dock_content)
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Введите команду для агента...")
        self.execute_button = QPushButton("Выполнить")
        dock_layout.addWidget(self.command_input)
        dock_layout.addWidget(self.execute_button)
        dock_layout.addStretch()
        self.command_dock.setWidget(dock_content)
        self.execute_button.clicked.connect(self.send_command_to_agent)
        self.command_input.returnPressed.connect(self.send_command_to_agent)

    def setup_ai_service(self):
        # ... (без изменений)
        self.ai_thread = QThread()
        self.ai_service = AIService()
        self.ai_service.moveToThread(self.ai_thread)
        self.ai_thread.started.connect(
            lambda: QTimer.singleShot(500, self.ai_service.initialize)
        )
        self.ai_service.create_frame_signal.connect(self.add_frame_to_scene)
        self.ai_thread.started.connect(lambda: print("[Main] AI Thread started."))
        self.ai_thread.start()

    def send_command_to_agent(self):
        # ... (без изменений)
        command = self.command_input.text()
        if command:
            self.command_input.clear()
            self.ai_service.execute_command(command)

    @pyqtSlot(dict)
    def add_frame_to_scene(self, frame_data: dict):
        print(f"[Main] Получен сигнал на создание фрейма: {frame_data}")
        frame_type = frame_data.get("type")
        params = frame_data.get("params", {})
        position = frame_data.get("position", {})

        new_frame = None
        if frame_type == "text_frame":
            new_frame = TextFrame(title=params.get("title"), content=params.get("content"))
        # --- НОВЫЙ БЛОК ДЛЯ WEB FRAME ---
        elif frame_type == "web_frame":
            new_frame = WebFrame(title=params.get("title"), url=params.get("url"))
        # --- КОНЕЦ НОВОГО БЛОКА ---
        else:
            print(f"[Main] Ошибка: неизвестный тип фрейма '{frame_type}'")

        if new_frame:
            new_frame.setPos(position.get("x", 0), position.get("y", 0))
            new_frame.setZValue(position.get("z", 0))
            self.scene.addItem(new_frame)

    def closeEvent(self, event):
        # ... (без изменений)
        print("[Main] Завершение работы AI потока...")
        self.ai_thread.quit()
        self.ai_thread.wait()
        super().closeEvent(event)