from PySide6.QtWidgets import QLineEdit, QVBoxLayout

from ui.widgets import Widget
from ui.theme import Theme, register_has_theme_and_apply


class LineEdit(Widget):

    def __init__(self, default: str = "", placeholder: str = "", parent=None):
        super().__init__(parent=parent)
        self.placeholder = placeholder

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self.qt_widget = QLineEdit()
        self.qt_widget.setText(default)
        self.qt_widget.setPlaceholderText(placeholder)
        self._layout.addWidget(self.qt_widget)

        self.text_changed = self.qt_widget.textChanged

        register_has_theme_and_apply(self)

    def get_text(self):
        return self.qt_widget.text()

    def set_placeholder(self, placeholder: str = ""):
        self.qt_widget.setPlaceholderText(placeholder)
        self.placeholder = placeholder

    def set_max_length(self, max_length: int):
        self.qt_widget.setMaxLength(max_length)

    def _apply_theme(self, theme: Theme):
        self.setStyleSheet(f"""
            QLineEdit {{
                color: {theme.text.color};
                background-color: {theme.surface.color};

                border: 2px solid {theme.border.color};
                border-radius: 4px;

                padding: 0px 4px;
                

                font-size: 13pt;
            }}

            QLineEdit:hover {{
                background-color: {theme.surface.color_double};
                border-color: {theme.border.color};
            }}

            QLineEdit:pressed {{
                background-color: {theme.surface.muted};
            }}

            QLineEdit:checked {{
                background-color: {theme.accent.color};
            }}

            QLineEdit:disabled {{
                color: {theme.text.muted};
                background-color: {theme.surface.muted};
                border-color: {theme.border.muted};
            }}""")
