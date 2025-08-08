# Файл: desk_agent/frames/base_frame.py
# ВЕРСИЯ: v10 (Масштабирование от курсора)

from PyQt6.QtWidgets import (
    QGraphicsProxyWidget, QWidget, QVBoxLayout, QLabel, QFrame,
    QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt, pyqtSlot, QPoint, QRectF
from PyQt6.QtGui import QFont, QCursor

class BaseFrame(QGraphicsProxyWidget):
    def __init__(self, title="Frame", parent=None):
        super().__init__(parent)

        self.main_widget = QFrame()
        self.main_widget.setMouseTracking(True)
        self.main_widget.setFrameShape(QFrame.Shape.Box)
        self.main_widget.setFrameShadow(QFrame.Shadow.Raised)
        self.main_widget.setStyleSheet("background-color: white; border: 1px solid #3498db;")
        self.main_widget.setMinimumSize(200, 150)

        self.layout = QVBoxLayout(self.main_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.title_bar = QWidget()
        self.title_bar.setStyleSheet("background-color: #3498db; color: white; border: none;")
        self.title_bar.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
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

        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        title_layout.addWidget(self.close_button)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)

        self.layout.addWidget(self.title_bar)
        self.layout.addWidget(self.content_widget, 1)

        self.setWidget(self.main_widget)

        self.setFlag(self.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(self.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.close_button.clicked.connect(self.close_frame)

        self.is_dragging = False
        self.is_resizing = False
        self.drag_offset = QPoint()
        self.border_margin = 10
        self.resize_edges = {"top": False, "bottom": False, "left": False, "right": False}

        self.setAcceptHoverEvents(True)

    @pyqtSlot()
    def close_frame(self):
        if self.scene():
            self.scene().removeItem(self)
        self.deleteLater()

    def _update_resize_edges(self, pos: QPoint):
        rect = self.widget().rect()
        self.resize_edges["top"] = abs(pos.y() - rect.top()) < self.border_margin
        self.resize_edges["bottom"] = abs(pos.y() - rect.bottom()) < self.border_margin
        self.resize_edges["left"] = abs(pos.x() - rect.left()) < self.border_margin
        self.resize_edges["right"] = abs(pos.x() - rect.right()) < self.border_margin

    def hoverMoveEvent(self, event):
        self._update_resize_edges(event.pos().toPoint())
        
        widget_cursor = QCursor(Qt.CursorShape.ArrowCursor)

        if (self.resize_edges["top"] and self.resize_edges["left"]) or \
           (self.resize_edges["bottom"] and self.resize_edges["right"]):
            widget_cursor = QCursor(Qt.CursorShape.SizeFDiagCursor)
        elif (self.resize_edges["top"] and self.resize_edges["right"]) or \
             (self.resize_edges["bottom"] and self.resize_edges["left"]):
            widget_cursor = QCursor(Qt.CursorShape.SizeBDiagCursor)
        elif self.resize_edges["top"] or self.resize_edges["bottom"]:
            widget_cursor = QCursor(Qt.CursorShape.SizeVerCursor)
        elif self.resize_edges["left"] or self.resize_edges["right"]:
            widget_cursor = QCursor(Qt.CursorShape.SizeHorCursor)
        
        self.widget().setCursor(widget_cursor)
        
        super().hoverMoveEvent(event)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.isAccepted():
            return

        if event.button() == Qt.MouseButton.LeftButton:
            self._update_resize_edges(event.pos().toPoint())
            is_on_edge = any(self.resize_edges.values())

            if is_on_edge:
                self.is_resizing = True
                self.resize_start_geometry = self.geometry()
                self.resize_start_pos = event.scenePos()
                event.accept()
                return

            if self.title_bar.rect().contains(event.pos().toPoint()):
                self.is_dragging = True
                self.drag_offset = self.pos() - event.scenePos()
                event.accept()
                return

    def mouseMoveEvent(self, event):
        if self.is_resizing:
            delta = event.scenePos() - self.resize_start_pos
            start_rect = self.resize_start_geometry
            new_rect = QRectF(start_rect)

            # --- НАЧАЛО ИЗМЕНЕНИЙ ---
            if self.resize_edges["left"]:
                new_rect.setLeft(start_rect.left() + delta.x())
            if self.resize_edges["right"]:
                new_rect.setRight(start_rect.right() + delta.x())
            if self.resize_edges["top"]:
                new_rect.setTop(start_rect.top() + delta.y())
            if self.resize_edges["bottom"]:
                new_rect.setBottom(start_rect.bottom() + delta.y())
            # --- КОНЕЦ ИЗМЕНЕНИЙ ---
            
            if new_rect.width() < self.widget().minimumWidth():
                # Если тянем левую грань, корректируем правую, чтобы сохранить мин. ширину
                if self.resize_edges["left"]:
                    new_rect.setLeft(new_rect.right() - self.widget().minimumWidth())
                else:
                    new_rect.setWidth(self.widget().minimumWidth())
            
            if new_rect.height() < self.widget().minimumHeight():
                # Аналогично для верхней грани
                if self.resize_edges["top"]:
                    new_rect.setTop(new_rect.bottom() - self.widget().minimumHeight())
                else:
                    new_rect.setHeight(self.widget().minimumHeight())

            self.setGeometry(new_rect)
            return

        if self.is_dragging:
            self.setPos(event.scenePos() + self.drag_offset)
            return
            
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.is_resizing = False
        self.is_dragging = False
        self.unsetCursor()
        self.widget().unsetCursor()
        super().mouseReleaseEvent(event)