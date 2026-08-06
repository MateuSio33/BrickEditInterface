from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from enum import Enum

from ui.widgets import Widget, Surface, Button, Label
from ui.components.brick.filter_selector import FilterSelector

import brickedit

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mainwindow import BrickEditInterface


ADD_BTN_ICON = QIcon.fromTheme("list-add")
NO_FILTERS_LABEL_ALLOW_ALL_IF_EMPTY = "No filters selected. All bricks are selected."
NO_FILTERS_LABEL = "No filters selected."

class BrickSelector(Widget):

    def __init__(self, mw: 'BrickEditInterface', allow_all_if_empty: bool = False, parent=None):
        super().__init__(parent=parent)

        self.mw = mw
        self.allow_all_if_empty = allow_all_if_empty

        self.true_master_layout = QVBoxLayout()
        self.true_master_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.true_master_layout)
        self.surface = Surface()
        # self.surface.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        self.true_master_layout.addWidget(self.surface)
        self.master_layout = self.surface.layout()

        self.add_button = Button("Add a filter", icon=ADD_BTN_ICON, tint_icon=True)
        self.add_button.clicked.connect(self.open_filter_selector)
        self.master_layout.addWidget(self.add_button)

        self.filter_selector = FilterSelector(parent=self)

        self.no_filters_label = Label(NO_FILTERS_LABEL_ALLOW_ALL_IF_EMPTY if self.allow_all_if_empty else NO_FILTERS_LABEL)
        # self.no_filters_label.hide()
        self.master_layout.addWidget(self.no_filters_label)



    def set_filters(self, filters: list):  # TODO fix annotations when filters are implemented
        pass


    def set_allow_all_if_empty(self, allow_all_if_empty: bool):
        self.allow_all_if_empty = allow_all_if_empty

    def is_allowed(self, brick: brickedit.Brick):
        return True  # TODO


    def open_filter_selector(self):
        pos = self.add_button.mapToGlobal(self.add_button.rect().bottomLeft())
        self.filter_selector.move(pos)
        self.filter_selector.show()
