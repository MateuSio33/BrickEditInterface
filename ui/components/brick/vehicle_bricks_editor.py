from PySide6.QtWidgets import QVBoxLayout

from ui.widgets import Widget, Switcher, Label
from ui.models import TooltipContents
from ui.components.brick.grouping_methods import *

from collections import defaultdict
from enum import Enum

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mainwindow import BrickEditInterface
    from ui.components.brick_filter.brick_selector import BrickSelector


GMS: list[BaseGM] = [
    NoGroupingGM(),
    TypeGM(),
    ClassGM(),
    EditorGroupGM(),
    WeldGroupGM(),
    MergeAllGM(),
]


class VehicleBricksEditor(Widget):

    def __init__(self,
        mw: 'BrickEditInterface',
        bs: 'BrickSelector',
        gm: BaseGM = GMS[0]
    ):
        super().__init__()
        self.mw = mw
        self.brick_selector = bs
        self.grouping_method = gm

        self.master_layout = QVBoxLayout(self)
        self.master_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.master_layout)

        self.grouping_method_switcher = Switcher([(e.get_name(), e.get_tooltip()) for e in GMS])
        self.master_layout.addWidget(self.grouping_method_switcher)

        self.no_bricks_selected = Label("No bricks selected.")
        self.master_layout.addWidget(self.no_bricks_selected)

        self.mw.vehicle_selector_banner.vehicle_loaded.connect(self.on_vehicle_loaded)
        self.brvfile = None
        self.on_vehicle_loaded()

        self._build()


    def on_vehicle_loaded(self):
        self.brvfile = self.mw.vehicle_selector_banner.get_brvfile_copy()


    def _build(self):

        if self.brvfile is None:
            return self._build_empty()

        filtered_bricks = [brick for brick in self.brvfile.bricks if self.brick_selector.is_allowed(brick)]
        if not filtered_bricks:
            return self._build_empty()

        self.no_bricks_selected.hide()

        properties = defaultdict(set)
        for brick in filtered_bricks:
            for prop, value in brick.get_all_properties() | brick.ppatch:
                properties[prop].add(value)


    def _build_empty(self):
        self.no_bricks_selected.show()

    # ----------


    def clear_changes_and_reload(self):
        pass

    def set_grouping_method(self, grouping_method: BaseGM):
        if grouping_method != self.grouping_method:
            self.grouping_method = grouping_method
            self._build()
