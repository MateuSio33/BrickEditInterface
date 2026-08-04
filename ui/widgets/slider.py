from PySide6.QtWidgets import QHBoxLayout, QSlider
from PySide6.QtCore import Qt

from ui.widgets import Widget
from ui.theme import Theme, register_has_theme_and_apply


class Slider(Widget):

    def __init__(self,
        values: list[object] | range | int,
        default_value: int = 0,
        ticks: bool = False,
        parent=None
    ):
        """If a list or range is passed, get_value can be used to get item at position.
        Range does not guarentee step size."""
        super().__init__(parent=parent)

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self.values = values
        self.ticks = ticks

        self.qt_widget = QSlider(Qt.Horizontal)
        if isinstance(self.values, list):
            self.qt_widget.setRange(0, len(self.values) - 1)
            self.qt_widget.setPageStep(5)
        elif isinstance(self.values, range):
            self.qt_widget.setRange(self.values.start, self.values.stop)
            self.qt_widget.setSingleStep(self.values.step)
            self.qt_widget.setPageStep(5 * self.values.step)
        else:
            self.qt_widget.setRange(0, self.values - 1)
            self.qt_widget.setPageStep(5)

        if ticks:
            self.qt_widget.setTickPosition(QSlider.TicksBelow)
        self.qt_widget.setValue(default_value)

        self.value_changed = self.qt_widget.valueChanged

        self._layout.addWidget(self.qt_widget)

        register_has_theme_and_apply(self)


    def set_value(self, value):
        return self.qt_widget.setValue(value)

    def get_position(self):
        return self.qt_widget.value()

    def get_value(self):
        if isinstance(self.values, list):
            return self.values[self.qt_widget.value()]
        return self.qt_widget.value()


    def _apply_theme(self, theme: Theme):

        # Rounded style
        # SLIDER_HEIGHT = 6
        # BORDER_THICKNESS = 2
        # BORDER_RADIUS = 5
        # HANDLE_WIDTH = 10
        # HANDLE_HEIGHT_OVER_GROOVE = 4
        # HANDLE_BORDER_RADIUS = 6

        # Rounded style with short handle
        # SLIDER_HEIGHT = 6
        # BORDER_THICKNESS = 2
        # BORDER_RADIUS = 5
        # HANDLE_WIDTH = 4
        # HANDLE_HEIGHT_OVER_GROOVE = 4
        # HANDLE_BORDER_RADIUS = 4

        # Square style
        SLIDER_HEIGHT = 6
        BORDER_THICKNESS = 2
        BORDER_RADIUS = 3
        HANDLE_WIDTH = 4
        HANDLE_HEIGHT_OVER_GROOVE = 4
        HANDLE_BORDER_RADIUS = 3

        self.setStyleSheet(f"""
            /* Entire groove (track) */
            QSlider::groove:horizontal {{
                border: {BORDER_THICKNESS}px solid {theme.border.color};
                height: {SLIDER_HEIGHT}px;
                background: {theme.surface.color};
                border-radius: {BORDER_RADIUS}px;
            }}
            
            QSlider::sub-page:horizontal {{
                background: {theme.accent_surface.color_double};
                border: {BORDER_THICKNESS}px solid {theme.accent_border.color};
                border-radius: {BORDER_RADIUS}px;
            }}

            QSlider::handle:horizontal {{
                width: {HANDLE_WIDTH}px;
                background: {theme.background.color};
                border: {BORDER_THICKNESS}px solid {theme.text.color};
                margin: -{HANDLE_HEIGHT_OVER_GROOVE}px 0;
                border-radius: {HANDLE_BORDER_RADIUS}px;
            }}
        """)
