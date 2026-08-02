from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtGui import QIcon

from ui.widgets import Widget
from ui.theme import Theme, register_has_theme_and_apply
from utils import tint_icon


class ColoredIcon(Widget):

    def __init__(self, qicon: QIcon, color: str, parent=None):

        super().__init__(parent=parent)

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self.og_qt_widget = qicon
        self.qt_widget = tint_icon(qicon, color)
        
        self._layout.addWidget(self.qt_widget)

        register_has_theme_and_apply(self)


    def set_color(self, color: str):
        self.qt_widget = tint_icon(self.og_qt_widget, color)
