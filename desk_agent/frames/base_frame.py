# Файл: desk_agent/desk_agent/frames/base_frame.py

from PyQt6.QtWidgets import (
    QGraphicsProxyWidget, QWidget, QVBoxLayout, QLabel, QFrame, 
    QPushButton, QHBoxLayout, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QFont, QCursor

class BaseFrame(QGraphicsProxyWidget):
    def __init__(self, title="Frame", parent=None):
        super().__init__(parent)
        
        # --- Основная настройка виджета (без изменений) ---
        self.main_widget = QFrame()
        self.main_widget.setFrameShape(QFrame.Shape.Box)
        self.main_widget.setFrameShadow(QFrame.Shadow.Raised)
        self.main_widget.setStyleSheet("background-color: white;")
        self.main_widget.setMinimumSize(200, 100)

        # --- НОВОЕ: Включаем отслеживание мыши для hover-событий ---
        self.main_widget.setMouseTracking(True)
        
        # --- Настройка лайаутов и заголовка (без изменений) ---
        self.layout = QVBoxLayout(self.main_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        self.title_bar = QWidget()
        self.title_bar.setStyleSheet("background-color: #3498db; color: white;")
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(5, 2, 2, 2)
        title_layout.setSpacing(5)

        self.title_label = QLabel(title)
        font = self.title_label.font()
        font.setBold(True)
        self.title_label.setFont(font)

        self.close_button = QPushButton("X")
        self.close_button.setStyleSheet("""
            QPushButton { background-color: #e74c3c; color: white; border: none; font-weight: bold; }
            QPushButton:hover { background-color: #c0392b; }
        """)
        self.close_button.setFixedSize(20, 20)
        self.close_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        title_layout.addWidget(self.close_button)
        
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)

        self.layout.addWidget(self.title_bar)
        self.layout.addWidget(self.content_widget)

        self.setWidget(self.main_widget)
        
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(self.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.close_button.clicked.connect(self.close_frame)

        # --- НОВОЕ: Состояния для перетаскивания и изменения размера ---
        self.is_resizing = False
        self.drag_start_pos = None
        self.resize_hotspot_size = 15 # Размер активной зоны в углу
        
        # Включаем hover-события для самого QGraphicsProxyWidget
        self.setAcceptHoverEvents(True)

    @pyqtSlot()
    def close_frame(self):
        # ... (без изменений)
        print(f"[Frame] Закрытие фрейма: {self.title_label.text()}")
        if self.scene():
            self.scene().removeItem(self)
        self.deleteLater()

    # --- НОВЫЕ И ОБНОВЛЕННЫЕ ОБРАБОТЧИКИ СОБЫТИЙ ---
    
    def _in_resize_hotspot(self, pos):
        """Проверяет, находится ли позиция в зоне изменения размера."""
        rect = self.widget().rect()
        return (rect.width() - self.resize_hotspot_size < pos.x() < rect.width() and
                rect.height() - self.resize_hotspot_size < pos.y() < rect.height())

    def hoverMoveEvent(self, event):
        """Вызывается при движении курсора над фреймом."""
        if self._in_resize_hotspot(event.pos().toPoint()):
            self.setCursor(QCursor(Qt.CursorShape.SizeFDiagCursor))
        else:
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        super().hoverMoveEvent(event)

    def mousePressEvent(self, event):
        """Вызывается при нажатии кнопки мыши."""
        pos_in_widget = event.pos().toPoint()
        
        # Сначала проверяем, не клик ли это для изменения размера
        if self._in_resize_hotspot(pos_in_widget) and event.button() == Qt.MouseButton.LeftButton:
            self.is_resizing = True
            self.resize_start_pos = event.pos()
            self.resize_start_size = self.widget().size()
            event.accept()
            return

        # Затем проверяем, не клик ли это для перетаскивания
        if self.title_label.rect().contains(self.title_label.mapFromGlobal(event.screenPos().toPoint())):
            self.drag_start_pos = self.pos() - event.scenePos()
            event.accept()
            return

        # Иначе передаем событие дальше
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Вызывается при движении мыши с зажатой кнопкой."""
        if self.is_resizing:
            delta = event.pos() - self.resize_start_pos
            new_size = self.resize_start_size + delta.toPoint()
            # Устанавливаем новый размер для вложенного виджета
            self.widget().resize(new_size)
            return

        if self.drag_start_pos is not None:
            self.setPos(self.drag_start_pos + event.scenePos())
            return
            
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Вызывается при отпускании кнопки мыши."""
        self.is_resizing = False
        self.drag_start_pos = None
        super().mouseReleaseEvent(event)