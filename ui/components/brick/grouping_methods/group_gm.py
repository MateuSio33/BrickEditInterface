from ui.components.brick.grouping_methods.base_gm import BaseGM
from ui.models import TooltipContents


GROUP_NAMING_TOOLTIP = TooltipContents("You can name any group (weld or editor) by creating a text brick (any type) and setting the text to\n<code>bei#&lt;my group name&gt;</code>")

class EditorGroupGM(BaseGM):
    @classmethod
    def get_name(cls):
        return "Split selection by editor groups"

    @classmethod
    def get_tooltip(cls) -> TooltipContents | None:
        return GROUP_NAMING_TOOLTIP

class WeldGroupGM(BaseGM):
    @classmethod
    def get_name(cls):
        return "Split selection by weld groups"

    @classmethod
    def get_tooltip(cls) -> TooltipContents | None:
        return GROUP_NAMING_TOOLTIP
