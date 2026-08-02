from PySide6.QtWidgets import QLabel, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from ui.widgets.widget import Widget
from ui.theme import Theme, register_has_theme_and_apply, theme_manager


class Label(Widget):

    def __init__(self, text: str | None = None,
        font_size = 13, font_weight = 400,
        muted = False,
        word_wrap = True,
        parent = None
    ):
        self.is_muted = muted
        super().__init__(parent)


        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self.qt_widget = QLabel(parent=self) if text is None else QLabel(text, parent=self)
        self.set_font_size(font_size)
        self.set_font_weight(font_weight)
        self.qt_widget.setWordWrap(word_wrap)

        self._layout.addWidget(self.qt_widget)
        # self.qt_widget.setAlignment(Qt.AlignCenter)
        
        self.qt_widget.setProperty('muted', self.is_muted)
        register_has_theme_and_apply(self)

    def set_muted(self, muted: bool):
        self.is_muted = muted
        self.qt_widget.setProperty('muted', muted)
        self._apply_theme(theme_manager.current())

    def set_text(self, text: str):
        self.qt_widget.setText(text)

    def set_font_size(self, size: int):
        font = self.qt_widget.font()
        font.setPointSize(size)
        self.qt_widget.setFont(font)

    def set_font_weight(self, weight: int):
        font = self.qt_widget.font()
        font.setWeight(QFont.Weight(weight))
        self.qt_widget.setFont(font)

    def set_bold(self, bold: bool):
        self.set_font_weight(700 if bold else 400)

    def set_italic(self, italic: bool):
        font = self.qt_widget.font()
        font.setItalic(italic)
        self.qt_widget.setFont(font)


    def _apply_theme(self, theme: Theme):
        # color = theme.text.muted if self.is_muted else theme.text.color
        self.setStyleSheet(f"""
            QLabel {{
                color: {theme.text.color};
            }}
            QLabel[muted=true] {{
                color: {theme.text.muted};
            }}
            """)



class HeaderLabel(Label):

    # px_size, top_margin, weight
    _LEVEL_TO_SIZE = {
        1: (26, 12, 700),
        2: (22, 10, 700),
        3: (18, 8,  700),
        4: (16, 7,  700),
        5: (14, 6,  700),
    }

    def __init__(self, text, level: int, center_text=False, margins_mult=1, parent=None):

        assert level in self._LEVEL_TO_SIZE
        px_size, top_margin, weight = self._LEVEL_TO_SIZE[level]

        super().__init__(text, px_size, weight, parent=parent)

        self.setContentsMargins(0, margins_mult * top_margin, 0, 0)

        if center_text:
            self.qt_widget.setAlignment(Qt.AlignCenter)
