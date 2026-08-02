from dataclasses import dataclass
from PySide6.QtCore import QObject, Signal
from typing import Protocol

from systems.settings import settings_manager


def make_muted_color_from_hex(col: str, brightness_mult: float = 0.75) -> str:
    col = col.lstrip('#').rjust(8, 'f')
    r, g, b, a = int(col[:2], 16), int(col[2:4], 16), int(col[4:6], 16), int(col[6:8], 16)
    # OLD:
    # max_cnl = max(r, g, b)
    # r2, g2, b2 = r/2 + max_cnl/4, g/2 + max_cnl/4, b/2 + max_cnl/4

    r2, g2, b2 = (r+128)//2 * brightness_mult, (g+128)//2 * brightness_mult, (b+128)//2 * brightness_mult
    r2, g2, b2 = min(int(r2), 255), min(int(g2), 255), min(int(b2), 255)

    return f"#{r2:02x}{g2:02x}{b2:02x}{a:02x}"


def calculate_alpha_stack(*alpha: int):
    transparency_product = 1
    for a in alpha:
        transparency_product *= (255-a)/255
    return int(255 - 255 * transparency_product)


class ThemeColor:
    def __init__(self, color: str, muted: str | None = None):
        self._r, self._g, self._b, self._a = self._parse_hex(color)
        if muted is not None:
            self._mr, self._mg, self._mb, self._ma = self._parse_hex(muted)
        else:
            self._mr, self._mg, self._mb, self._ma = self._mute(self._r, self._g, self._b, self._a)

        self._color_double = self._stack_alpha_rgba(self._r, self._g, self._b, self._a, 2)
        self._muted_double = self._stack_alpha_rgba(self._mr, self._mg, self._mb, self._ma, 2)

    @staticmethod
    def _parse_hex(col: str) -> tuple[int, int, int, int]:
        col = col.lstrip('#')
        if len(col) == 6:
            col += 'ff'          # default to fully opaque when alpha omitted
        r, g, b, a = int(col[0:2], 16), int(col[2:4], 16), int(col[4:6], 16), int(col[6:8], 16)
        return r, g, b, a

    @staticmethod
    def _mute(r, g, b, a, brightness_mult: float = 0.75) -> tuple[int, int, int, int]:
        r2 = min(int((r + 128) // 2 * brightness_mult), 255)
        g2 = min(int((g + 128) // 2 * brightness_mult), 255)
        b2 = min(int((b + 128) // 2 * brightness_mult), 255)
        return r2, g2, b2, a

    @staticmethod
    def _stack_alpha_rgba(r, g, b, a, times: int) -> str:
        stacked = a
        for _ in range(times - 1):
            stacked = calculate_alpha_stack(stacked, a)
        return f"rgba({r}, {g}, {b}, {stacked})"

    @property
    def color(self) -> str: return f"rgba({self._r}, {self._g}, {self._b}, {self._a})"
    @property
    def color_hex_rgba(self) -> str: return f"#{self._r:02x}{self._g:02x}{self._b:02x}{self._a:02x}"
    @property
    def color_hex_argb(self) -> str: return f"#{self._a:02x}{self._r:02x}{self._g:02x}{self._b:02x}"

    @property
    def muted(self) -> str: return f"rgba({self._mr}, {self._mg}, {self._mb}, {self._ma})"
    @property
    def muted_hex_rgba(self) -> str: return f"#{self._mr:02x}{self._mg:02x}{self._mb:02x}{self._ma:02x}"
    @property
    def muted_hex_argb(self) -> str: return f"#{self._ma:02x}{self._mr:02x}{self._mg:02x}{self._mb:02x}"

    @property
    def color_double(self) -> str:
        """Color whose transparency is adjusted to simulate being applied twice"""
        return self._color_double

    @property
    def muted_double(self) -> str:
        """Muted color whose transparency is adjusted to simulate being applied twice"""
        return self._muted_double

    def color_advanced(self, alpha_stack: int = 1, hex: bool = False):
        alpha = calculate_alpha_stack(*[self._a for _ in range(alpha_stack)]) if alpha_stack != 1 else self._a
        if hex:
            return f"#{alpha:02x}{self._r:02x}{self._g:02x}{self._b:02x}"
        else:
            return f"rgba({self._r}, {self._g}, {self._b}, {alpha})"

    def muted_advanced(self, alpha_stack: int = 1, hex: bool = False):
        alpha = calculate_alpha_stack(*[self._ma for _ in range(alpha_stack)]) if alpha_stack != 1 else self._ma
        if hex:
            return f"#{alpha:02x}{self._mr:02x}{self._mg:02x}{self._mb:02x}"
        else:
            return f"rgba({self._mr}, {self._mg}, {self._mb}, {alpha})"


@dataclass(frozen=True)
class Theme:
    name: str
    display_name: str
    is_highcontrast: bool

    background: ThemeColor
    sidebar: ThemeColor
    surface: ThemeColor
    border: ThemeColor
    text: ThemeColor
    accent: ThemeColor
    accent_surface: ThemeColor
    accent_border: ThemeColor
    danger: ThemeColor
    danger_surface: ThemeColor
    danger_border: ThemeColor


DARK = Theme(name="dark", display_name="Dark mode", is_highcontrast=False,
    background=ThemeColor("#101420ff"),
    sidebar=ThemeColor("#1b2238ff"),
    surface=ThemeColor("#80809030"),
    border=ThemeColor("#5b5b64ff"),
    text=ThemeColor("#f8ebe0ff"),
    accent=ThemeColor("#dd4433ff"),
    accent_surface=ThemeColor("#dd443350"),
    accent_border=ThemeColor("#ff8866ff"),
    danger=ThemeColor("#ee2830ff"),
    danger_surface=ThemeColor("#ee283050"),
    danger_border=ThemeColor("#ac191eff")
)
LIGHT = Theme(name="light", display_name="Light mode", is_highcontrast=False,
    background = ThemeColor("#ebe9e7ff"),
    sidebar=ThemeColor("#dddbd8ff"),
    surface=ThemeColor("#ffffff80", "#80808040"),
    border=ThemeColor("#b8b4b0ff"),
    text=ThemeColor("#303660ff", "#64677aff"),
    accent=ThemeColor("#ee5544ff"),
    accent_surface=ThemeColor("#dd443350"),
    accent_border=ThemeColor("#aa3322ff"),
    danger=ThemeColor("#ee2830ff"),
    danger_surface=ThemeColor("#ee283050"),
    danger_border=ThemeColor("#ac191eff")
)
NIGHT = Theme(name="night", display_name="Night mode", is_highcontrast=False,
    background = ThemeColor("#000000ff"),
    sidebar=ThemeColor("#000000ff"),
    surface=ThemeColor("#60607840"),
    border=ThemeColor("#4b4b50ff"),
    text=ThemeColor("#f8ebe0ff"),
    accent=ThemeColor("#dd4433ff"),
    accent_surface=ThemeColor("#dd443350"),
    accent_border=ThemeColor("#ff8866ff"),
    danger=ThemeColor("#ee2830ff"),
    danger_surface=ThemeColor("#ee283050"),
    danger_border=ThemeColor("#ac191eff")
)
HIGH_CONTRAST = Theme(name="highcontrast", display_name="High contrast", is_highcontrast=True,
    background=ThemeColor("#000000ff"),
    sidebar=ThemeColor("#000000ff"),
    surface=ThemeColor("#ffffff20"),
    border=ThemeColor("#ffffffff"),
    text=ThemeColor("#ffffffff"),
    accent=ThemeColor("#dd4433ff"),
    accent_surface=ThemeColor("#dd443350"),
    accent_border=ThemeColor("#ffc0b8ff"),
    danger=ThemeColor("#ee2830ff"),
    danger_surface=ThemeColor("#ee283050"),
    danger_border=ThemeColor("#ac191eff")
)
DEV_TEST = Theme(name="dev", display_name="Developer test", is_highcontrast=False,
    background=ThemeColor("#000040ff"),
    sidebar=ThemeColor("#000080ff"),
    surface=ThemeColor("#8080ff30"),
    border=ThemeColor("#8080ffff"),
    text=ThemeColor("#ffff80ff"),
    accent=ThemeColor("#dd4433ff"),
    accent_surface=ThemeColor("#dd443350"),
    accent_border=ThemeColor("#ff8866ff"),
    danger=ThemeColor("#ee2830ff"),
    danger_surface=ThemeColor("#ee283050"),
    danger_border=ThemeColor("#ac191eff")
)

class ThemeManager(QObject):
    theme_changed = Signal(object)  # emits a Theme
    themes = (DARK, LIGHT, NIGHT, HIGH_CONTRAST, DEV_TEST)

    def __init__(self):
        super().__init__()

        self._current = DARK
        self.set_theme_from_name(settings_manager.theme)

    def current(self) -> Theme:
        """Returns current theme object."""
        return self._current

    def set_theme(self, theme: Theme) -> None:
        """Sets current theme and update all widgets."""
        self._current = theme
        settings_manager.theme = theme.name
        settings_manager.save()
        self.theme_changed.emit(theme)

    def set_theme_from_name(self, name: str) -> None:
        for theme in self.themes:
            if theme.name != name:
                continue
            self.set_theme(theme)

theme_manager = ThemeManager()


class SupportsTheme(Protocol):
    def _apply_theme(self, theme: Theme) -> None:
        ...

def reapply_theme(target: SupportsTheme):
    target._apply_theme(theme_manager.current())

def register_has_theme_and_apply(target: SupportsTheme, theme_manager: Theme = theme_manager):
    """Registers anything which supports themes """
    theme_manager.theme_changed.connect(target._apply_theme)
    target._apply_theme(theme_manager.current())
