from PySide6.QtWidgets import QScrollArea
from PySide6.QtCore import QSize

class ContentSizedScrollArea(QScrollArea):
    def __init__(self, max_height=275, parent=None):
        super().__init__(parent)
        self.max_height = max_height

    def sizeHint(self):
        w = self.widget()
        if w is None:
            return super().sizeHint()
        hint = w.sizeHint()
        return QSize(hint.width(), min(hint.height(), self.max_height))
