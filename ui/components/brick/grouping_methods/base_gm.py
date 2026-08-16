from ui.models import TooltipContents

class BaseGM:

    @classmethod
    def get_name(cls):
        return NotImplementedError(f"Subclass {cls.__name__} must implement get_name()")

    @classmethod
    def get_tooltip(cls) -> TooltipContents | None:
        return None
