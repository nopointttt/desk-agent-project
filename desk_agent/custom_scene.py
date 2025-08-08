from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtGui import QColor, QPen
from PyQt6.QtCore import Qt

class GridScene(QGraphicsScene):
    """
    Кастомная QGraphicsScene с отрисовкой сетки на фоне.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_size = 20  # Размер ячейки сетки
        self.grid_color = QColor(60, 60, 60, 51)  # Цвет сетки с 20% непрозрачностью

    def drawBackground(self, painter, rect):
        """
        Переопределенный метод для отрисовки фона. Вызывается автоматически.
        :param painter: QPainter для рисования.
        :param rect: Видимая область сцены (QRectF).
        """
        super().drawBackground(painter, rect)

        # Получаем текущий уровень зума из трансформации вида
        # m11() - это коэффициент масштабирования по горизонтали
        zoom_level = painter.worldTransform().m11()

        # Адаптивная толщина линий (Принцип LOD - Level of Detail)
        # При сильном отдалении линии становятся толще, чтобы оставаться видимыми
        pen_width = 1.0 / zoom_level
        
        pen = QPen(self.grid_color)
        pen.setWidthF(pen_width)
        painter.setPen(pen)

        # Определяем границы отрисовки с запасом
        left = int(rect.left()) - int(rect.left()) % self.grid_size
        top = int(rect.top()) - int(rect.top()) % self.grid_size

        # Рисуем вертикальные линии
        x = left
        while x < rect.right():
            painter.drawLine(int(x), int(rect.top()), int(x), int(rect.bottom()))
            x += self.grid_size

        # Рисуем горизонтальные линии
        y = top
        while y < rect.bottom():
            painter.drawLine(int(rect.left()), int(y), int(rect.right()), int(y))
            y += self.grid_size