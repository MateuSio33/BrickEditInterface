from PySide6.QtWidgets import QVBoxLayout

from ui.widgets import Widget
from ui.components.brick.property_widgets import get_property_widget

from utils import clear_layout

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.components.brick_filter.brick_selector import BrickSelector


class PropertySet(Widget):

    def __init__(self, bs: 'BrickSelector', properties: dict[str, set]):
        super().__init__()

        self.bs = bs

        self.master_layout = QVBoxLayout()
        self.master_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.master_layout)

        self.properties_layout = QVBoxLayout()
        self.properties_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.properties_layout)

        self.set_property_set(properties)


    def set_property_set(self, properties: dict[str, set]):
        clear_layout(self.properties_layout)

        sorted_properties: list[tuple[str, set]] = sorted([(k, v) for k, v in properties.items()], key=lambda x: x[0])

        for (prop, values) in sorted_properties:

            formula_mode = len(values) > 1
            if len(values) == 0:
                continue

            widget = get_property_widget(prop, values, formula_mode, None if formula_mode else values[0], show_text=False)
            if widget is None:
                continue

            self.properties_layout.addWidget(widget)
