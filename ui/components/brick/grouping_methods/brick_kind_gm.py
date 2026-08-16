from ui.components.brick.grouping_methods.base_gm import BaseGM
from ui.models import TooltipContents


class TypeGM(BaseGM):
    @classmethod
    def get_name(cls):
        return "Split selection by type"

    @classmethod
    def get_tooltip(cls) -> TooltipContents | None:
        return TooltipContents("\"Brick types\" refer to the specific brick types (eg. Scalable Cubes, Scalable Wedges etc.) while \"brick classes\" refer to similar brick types (eg. Scalables, Lights etc.)")


class ClassGM(BaseGM):
    @classmethod
    def get_name(cls):
        return "Split selection by class"

    @classmethod
    def get_tooltip(cls) -> TooltipContents | None:
        return TooltipContents("\"Brick types\" refer to the specific brick types (eg. Scalable Cubes, Scalable Wedges etc.) while \"brick classes\" refer to similar brick types (eg. Scalables, Lights etc.)")
