from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal

from ui.widgets import Widget, ToolButton, Label
from ui.models import TooltipContents



class Switcher(Widget):

    index_changed = Signal(int)

    left_arrow_icon = None
    right_arrow_icon = None

    def __init__(self, items: list[str | tuple[str, TooltipContents | None]], idx: int = 0, looping: bool = False, parent=None):
        super().__init__(parent)
        self.items = [item[0] if isinstance(item, tuple) else item for item in items]
        self.tooltips = [item[1] if isinstance(item, tuple) else None for item in items]
        self.idx = idx
        self.looping = looping
        self.enabled = True

        self.master_layout = QHBoxLayout()
        self.master_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.master_layout)

        if self.left_arrow_icon is None:
            self.left_arrow_icon = QIcon(":/assets/icons/ArrowLeftSmallIcon.png")
            self.right_arrow_icon = QIcon(":/assets/icons/ArrowRightSmallIcon.png")

        self.left_arrow = ToolButton(self.left_arrow_icon, tint_icon = True, parent=self)
        self.left_arrow.clicked.connect(lambda: self.move_index(-1))
        self.right_arrow = ToolButton(self.right_arrow_icon, tint_icon = True, parent=self)
        self.right_arrow.clicked.connect(lambda: self.move_index(1))

        self.label = Label(center_text=True)

        self.master_layout.addWidget(self.left_arrow)
        self.master_layout.addWidget(self.label, stretch=1)
        self.master_layout.addWidget(self.right_arrow)

        self.set_index(self.idx)


    def set_enabled(self, enabled: bool):
        self.enabled = enabled
        self.left_arrow.set_enabled(enabled)
        self.right_arrow.set_enabled(enabled)
        self.label.set_muted(not enabled)


    def get_idx(self) -> int | None:
        return self.idx if self.items else None


    def set_items(self, items: list[str | tuple[str, TooltipContents]], idx: int | None = None):
        self.items = [item[0] if isinstance(item, tuple) else item for item in items]
        self.tooltips = [item[1] if isinstance(item, tuple) else None for item in items]
        idx = idx if idx is not None else self.idx
        self.set_index(idx)  # Will update the label


    def move_index(self, delta):
        self.set_index(self.idx + delta)


    def set_index(self, idx):
        if self.looping:
            self.idx = idx % len(self.items) if self.items else idx
        else:
            self.idx = 0 if idx < 0 else idx if idx < len(self.items) else len(self.items) - 1 if self.items else 0

        # Update label
        if len(self.items) == 0:
            self.label.set_text("None")
            self.label.set_tooltip(None)
            self.label.set_muted(True)
        else:
            self.label.set_text(self.items[self.idx])
            self.label.set_tooltip(self.tooltips[self.idx])
            self.label.set_muted(not self.enabled)

        # Update buttons
        self.left_arrow.set_enabled(self.enabled and self.looping or self.idx != 0)
        self.right_arrow.set_enabled(self.enabled and self.looping or self.idx < len(self.items) - 1)

        self.index_changed.emit(self.idx)
