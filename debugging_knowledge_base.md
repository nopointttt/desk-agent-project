## Case ID: 20250804-193200

**Ошибка (Error):**
Функциональный сбой. Перемещение (`drag`) элемента `BaseFrame` и панорамирование (`pan`) фона в `QGraphicsView` не работали. Диагностические `print`-сообщения показали, что события мыши получал только `QGraphicsView`, но не его дочерний элемент `QGraphicsProxyWidget` (`BaseFrame`).

**Контекст (Context):**
* Версии файлов на момент 19-го шага:
    * `main_window.py`: 20:51:00
    * `custom_view.py`: 20:49:46
    * `base_frame.py`: 20:40:57
* Действия для воспроизведения: Клик и перетаскивание левой кнопкой мыши как на фоне, так и на элементе `BaseFrame`.

**Причина (Root Cause):**
Стандартный обработчик `QGraphicsView.mousePressEvent` (вызываемый через `super()`) перехватывал событие мыши для своей внутренней логики (например, для обработки выделения `ItemIsSelectable`) и останавливал его дальнейшее распространение (propagation) к дочерним элементам сцены. В результате `mousePressEvent` самого `BaseFrame` никогда не вызывался.

**Решение (Solution):**
В `BaseFrame.mousePressEvent` необходимо было "забрать" событие себе до того, как его обработает `QGraphicsView`. Это достигается вызовом `event.accept()` и немедленным выходом из функции, если событие предназначено для перемещения фрейма (клик по заголовку).

```python
# Фрагмент кода из frames/base_frame.py
def mousePressEvent(self, event):
    # Если клик левой кнопкой на заголовке - начинаем перетаскивание
    if event.button() == Qt.MouseButton.LeftButton and self.title_bar.rect().contains(event.pos().toPoint()):
        self.drag_start_pos = self.pos() - event.scenePos()
        event.accept() # <-- КЛЮЧЕВОЕ ИЗМЕНЕНИЕ: Забираем событие себе
        return         # <-- и выходим, не передавая его дальше
    # Если клик не на заголовке, передаем его стандартному обработчику
    super().mousePressEvent(event)