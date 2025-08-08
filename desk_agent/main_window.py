from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QLineEdit, QPushButton, QDockWidget
)
from PyQt6.QtCore import Qt, QThread, pyqtSlot, QTimer

# ИЗМЕНЕНИЕ: Импортируем конкретные имена
from .constants import TEXT_FRAME, WEB_FRAME
from .custom_scene import GridScene
from .custom_view import ZoomableView
from .ai_service import AIService
from .frame_factory import FrameFactory

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DESK Агент")
        self.setGeometry(100, 100, 1280, 720)

        self.scene = GridScene()
        self.graphics_view = ZoomableView(self.scene)
        self.setCentralWidget(self.graphics_view)
        
        self.frame_factory = FrameFactory()
        self.setup_command_interface()
        self.setup_ai_service()
        
        self.statusBar().showMessage("Агент готов к работе.")

    # ... (методы setup_command_interface, setup_ai_service, send_command_to_agent, show_notification без изменений) ...
    def setup_command_interface(self):
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
        self.ai_thread = QThread()
        self.ai_service = AIService()
        self.ai_service.moveToThread(self.ai_thread)
        self.ai_thread.started.connect(
            lambda: QTimer.singleShot(500, self.ai_service.initialize)
        )
        self.ai_service.create_frame_signal.connect(self.add_frame_to_scene)
        self.ai_service.show_notification_signal.connect(self.show_notification)
        self.ai_thread.started.connect(lambda: print("[Main] AI Thread started."))
        self.ai_thread.start()

    def send_command_to_agent(self):
        command = self.command_input.text()
        if command:
            self.command_input.clear()
            self.ai_service.execute_command(command)

    @pyqtSlot(str)
    def show_notification(self, message: str):
        print(f"[Main] Показ уведомления: {message}")
        self.statusBar().showMessage(message, 5000)

    @pyqtSlot(dict)
    def add_frame_to_scene(self, frame_data: dict):
        print(f"[Main] Получен сигнал на создание фрейма: {frame_data}")
        frame_type = frame_data.get("type")
        params = frame_data.get("params", {})
        position = frame_data.get("position", {})
        
        # ИЗМЕНЕНИЕ: Сравниваем с импортированными именами
        # Этот if/elif блок все еще здесь, но он больше не нужен, так как фабрика делает то же самое.
        # Оставим его для ясности, но фабрика - более правильный подход.
        # В идеале, этот блок должен быть заменен вызовом фабрики.
        # Давайте сделаем это правильно.
        
        new_frame = self.frame_factory.create_frame(frame_type, params)

        if new_frame:
            new_frame.setPos(position.get("x", 0), position.get("y", 0))
            new_frame.setZValue(position.get("z", 0))
            self.scene.addItem(new_frame)
        else:
            print(f"[Main] Ошибка: Фабрика не смогла создать фрейм типа '{frame_type}'")

    def closeEvent(self, event):
        print("[Main] Завершение работы AI потока...")
        self.ai_thread.quit()
        self.ai_thread.wait()
        super().closeEvent(event)