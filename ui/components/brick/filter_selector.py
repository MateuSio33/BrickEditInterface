from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt

from ui.widgets import Widget, Button, Label, ComboBox
from ui.theme import Theme, register_has_theme_and_apply
from ui.models import TooltipContents


FILTER_MODE_TOOLTIP = TooltipContents(text="""\
Filters can have 2 different modes:
<ul>
  <li>Should: Matching bricks are included, unless another filter removes them.</li>
  <li>Must: Bricks must match this filter, or they are removed.</li>
</ul>
Filters can be negated (Should/Must not), in which case bricks match this filter if the condition is not met.\
""")

OR_FILTER = "Should", "should"
NOR_FILTER = "Should not", "should not"
AND_FILTER = "Must", "must"
NAND_FILTER = "Must not", "must not"


class FilterSelector(Widget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("filter_selector", True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowFlags(Qt.Popup)

        self.master_layout = QVBoxLayout(self)
        self.setLayout(self.master_layout)


        # Filter mode
        self.filter_mode_layout = QHBoxLayout()
        self.filter_mode_layout.setContentsMargins(0, 0, 0, 0)
        self.master_layout.addLayout(self.filter_mode_layout)

        self.filter_mode_label = Label("Mode")
        self.filter_mode_label.set_tooltip(FILTER_MODE_TOOLTIP)
        self.filter_mode_layout.addWidget(self.filter_mode_label)

        self.filter_mode_combo_box = ComboBox()
        self.filter_mode_combo_box.add_item(OR_FILTER[0])
        self.filter_mode_combo_box.add_item(NOR_FILTER[0])
        self.filter_mode_combo_box.add_item(AND_FILTER[0])
        self.filter_mode_combo_box.add_item(NAND_FILTER[0])
        self.filter_mode_layout.addWidget(self.filter_mode_combo_box)


        register_has_theme_and_apply(self)


    def _apply_theme(self, theme: Theme):
        self.setStyleSheet(f"""
            *[filter_selector] {{
                background-color: {theme.background.color};

                border: 2px solid {theme.border.color};
                border-radius: 4px;
            }}
        """)
