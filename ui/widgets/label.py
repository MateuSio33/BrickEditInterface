from PySide6.QtWidgets import QLabel, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QFont, QIcon, QPainter, QPixmap

from ui.widgets.widget import Widget
from ui.theme import Theme, register_has_theme_and_apply, reapply_theme
from ui.models import TooltipContents

from utils import tint_icon


class _QLabel(QLabel):
    """QLabel that paints a small icon flush against the end of the last line of text."""

    ICON_TEXT_MARGIN = 5    # px between text and icon
    ICON_VERTICAL_OFFSET = 0  # px to nudge icon up(-) or down(+) relative to vertical centre

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._icon_pixmap: QPixmap | None = None
        self._icon_size: int = 11
        self._icon_visible: bool = False

    def set_icon(self, pixmap: QPixmap | None, size: int):
        self._icon_pixmap = pixmap
        self._icon_size = size
        self._update_margins()
        self.update()

    def set_icon_visible(self, visible: bool):
        self._icon_visible = visible
        self._update_margins()
        self.update()

    def _update_margins(self):
        showing = self._icon_visible and self._icon_pixmap is not None
        r = self._icon_size + self.ICON_TEXT_MARGIN if showing else 0
        self.setContentsMargins(0, 0, r, 0)

    def _last_line_end_x(self) -> int:
        """Use QTextLayout to accurately find where the last line of wrapped text ends."""
        from PySide6.QtGui import QTextLayout, QTextOption

        text = self.text()
        cr = self.contentsRect()

        option = QTextOption()
        if self.wordWrap():
            option.setWrapMode(QTextOption.WrapMode.WordWrap)
        else:
            option.setWrapMode(QTextOption.WrapMode.NoWrap)
        option.setAlignment(self.alignment())

        layout = QTextLayout(text, self.font())
        layout.setTextOption(option)
        layout.beginLayout()

        last_line = None
        y = 0.0
        while True:
            line = layout.createLine()
            if not line.isValid():
                break
            line.setLineWidth(cr.width())
            line.setPosition(QPointF(0, y))
            y += line.height()
            last_line = line

        layout.endLayout()

        if last_line is None:
            return 0

        return int(last_line.cursorToX(last_line.textLength())[0])

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self._icon_visible or self._icon_pixmap is None:
            return

        fm = self.fontMetrics()
        cr = self.contentsRect()

        last_line_x = self._last_line_end_x()
        x = cr.left() + last_line_x + self.ICON_TEXT_MARGIN

        # Vertically align to the last line's centre
        # Count lines by re-using layout height vs single line height
        line_height = fm.height()
        y = cr.top() + max(0, cr.height() - line_height) + \
            (line_height - self._icon_size) // 2 + self.ICON_VERTICAL_OFFSET

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.drawPixmap(x, y, self._icon_pixmap.scaled(
            self._icon_size, self._icon_size,
            Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))
        painter.end()



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
        self.setLayout(self._layout)

        self.qt_widget = _QLabel(parent=self) if text is None else _QLabel(text, parent=self)
        self.set_font_size(font_size)
        self.set_font_weight(font_weight)
        self.qt_widget.setWordWrap(word_wrap)

        self.tooltip_widget = None  # kept for API compat, no longer a real widget
        self.tooltip_enabled = False

        self._layout.addWidget(self.qt_widget)

        self.qt_widget.setProperty('muted', self.is_muted)

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
        self._update_tooltip_widget()

    def set_hide_tooltip_indicator(self, hide: bool):
        self.tooltip_enabled = hide
        self._update_tooltip_widget()

    def set_alignment(self, *args, **kwargs):
        return self.qt_widget.setAlignment(*args, **kwargs)

    def _update_tooltip_widget(self):
        self.tooltip_widget = True  # flag so callers using `is not None` still work
        self.qt_widget.set_icon_visible(self.tooltip_enabled)

    def _apply_theme(self, theme: Theme):
        pixmap = tint_icon(
            self.info_icon, theme.text.color_hex_argb, size=self.info_icon_size
        ).pixmap(self.info_icon_size)
        self.qt_widget.set_icon(pixmap, self.info_icon_size)

        self.setStyleSheet(f"""
            QLabel {{
                color: {theme.text.color};
            }}
            QLabel[muted=true] {{
                color: {theme.text.muted};
            }}
        """)


class HeaderLabel(Label):

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
