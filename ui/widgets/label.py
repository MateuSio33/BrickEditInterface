from PySide6.QtWidgets import QLabel, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon

from ui.widgets.widget import Widget
from ui.theme import Theme, register_has_theme_and_apply, reapply_theme
from ui.models import TooltipContents

from utils import tint_icon


class Label(Widget):

    info_icon_size = 11
    info_icon = None

    def __init__(self, text: str | None = None,
        font_size = 13, font_weight = 400,
        muted = False,
        word_wrap = True,
        parent = None
    ):
        self.is_muted = muted
        super().__init__(parent)


        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setAlignment(Qt.AlignLeft)
        self.setLayout(self._layout)

        self.qt_widget = QLabel(parent=self) if text is None else QLabel(text, parent=self)
        self.set_font_size(font_size)
        self.set_font_weight(font_weight)
        self.qt_widget.setWordWrap(word_wrap)

        self.tooltip_widget = None
        self.tooltip_enabled = False

        self._layout.addWidget(self.qt_widget)
        # self.qt_widget.setAlignment(Qt.AlignCenter)
        
        self.qt_widget.setProperty('muted', self.is_muted)

        # almost static stuff
        if self.info_icon is None:
            self.info_icon = QIcon(':/assets/icons/Information.png')

        register_has_theme_and_apply(self)

    def set_muted(self, muted: bool):
        self.is_muted = muted
        self.qt_widget.setProperty('muted', muted)
        reapply_theme(self)

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

    def set_tooltip(self, tooltip: TooltipContents | None):
        if tooltip is None:
            self.setToolTip("")
            self.tooltip_enabled = False
        else:
            self.setToolTip(tooltip.richtext())
            self.tooltip_enabled = True
        self._update_tooltip_widget()  # Make and show widget if it doesn't exist yet

    def set_hide_tooltip_indicator(self, hide: bool):
        self.tooltip_enabled = hide
        self._update_tooltip_widget()


    def _update_tooltip_widget(self):
        if self.tooltip_widget is not None:
            if self.tooltip_enabled:
                self.tooltip_widget.show()
            else:
                self.tooltip_widget.hide()
            return

        self.tooltip_widget = QLabel()
        reapply_theme(self)
        self._layout.addWidget(self.tooltip_widget, alignment=Qt.AlignBaseline)


    def _apply_theme(self, theme: Theme):
        # color = theme.text.muted if self.is_muted else theme.text.color
        if self.tooltip_widget is not None:
            self.tooltip_widget.setPixmap(tint_icon(self.info_icon, theme.text.color_hex_argb, size=self.info_icon_size).pixmap(self.info_icon_size))

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
