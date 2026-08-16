from ui.components.brick.grouping_methods.base_gm import BaseGM
from ui.models import TooltipContents

class NoGroupingGM(BaseGM):
    @classmethod
    def get_name(cls):
        return "Split selection by individual bricks"

class MergeAllGM(BaseGM):
    @classmethod
    def get_name(cls):
        return "Do not split selection"

    @classmethod
    def get_tooltip(cls) -> TooltipContents | None:
        return TooltipContents("Edit all selected bricks simultaneously")
