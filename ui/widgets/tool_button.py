from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QToolButton, QSizePolicy, QVBoxLayout

from ui.widgets.widget import Widget
from ui.theme import Theme, register_has_theme_and_apply


class ToolButton(Widget):

    def __init__(self, icon: QIcon | None = None, parent=None):
        super().__init__(parent)

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self.qt_widget = QToolButton()
        self._layout.addWidget(self.qt_widget)

        self.clicked = self.qt_widget.clicked
        self.toggled = self.qt_widget.toggled

        self.qt_widget.setAutoRaise(False)
        self.qt_widget.setToolButtonStyle(
            Qt.ToolButtonIconOnly
        )

        self.qt_widget.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.Fixed,
        )
        if icon:
            self.set_icon(icon)
        self.set_button_size(26)
        
        register_has_theme_and_apply(self)


    def set_icon(self, icon: QIcon):
        self.qt_widget.setIcon(icon)

    def set_icon_from_theme(self, *names: str):
        for name in names:
            icon = QIcon.fromTheme(name)
            if not icon.isNull():
                self.qt_widget.setIcon(icon)
                return True
        return False

    def set_button_size(self, size: int):
        self.qt_widget.setFixedSize(size, size)
        self.qt_widget.setIconSize(QSize(size - 8, size - 8))

    def _apply_theme(self, theme: Theme):
        
            self.setStyleSheet(f"""
            QToolButton {{
                color: {theme.text.color};
                background-color: {theme.surface.color};

                border: 2px solid {theme.border.color};
                border-radius: 4px;

                padding: 1px 4px;

                font-size: 13pt;
            }}

            QToolButton:hover {{
                background-color: {theme.surface.color_double};
                border-color: {theme.border.color};
            }}

            QToolButton:pressed {{
                background-color: {theme.surface.muted};
            }}

            QToolButton:checked {{
                background-color: {theme.accent.color};
            }}

            QToolButton:disabled {{
                color: {theme.text.muted};
                background-color: {theme.surface.muted};
                border-color: {theme.border.muted};
            }}""")
