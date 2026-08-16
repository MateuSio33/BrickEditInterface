from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Signal

from ui.widgets import Widget, Switcher, StyledLabel, LabelStyle, Slider, LineEdit, NumberChannelEdit, FormulaChannelEdit, ComboBox
from ui.components.brick.property_utils import get_or_make_property_display_name

from utils import Sentinel

from typing import Hashable, TypeVar

import brickedit


NOT_EDITED = Sentinel("NOT_EDITED")


T = TypeVar("T", bound=Hashable)



class BasePropertyWidget(Widget):

    value_changed = Signal(tuple)

    def __init__(self, property_name: str, test_values: tuple[T, ...], formula_mode: bool, initial_value: T, enabled: bool = True, show_text: bool = True):
        """Property name is the internal property name from brick rigs (eg. bGenerateLift).

        Test values is a set of values that must be tested for whne evaluating a widget. Eg. when
        a user inputs a formula like 1/(x-1), this formula may yield invalid numbers if eg. x is 1.
        If any of these test values cause an error, then the input will not be allowed.

        Test values are not guarenteed to be used as they are irrelevant for some property types
        such as booleans."""
        super().__init__()

        self.property_name = property_name
        self.test_values = test_values
        self.formula_mode = formula_mode
        self.value = NOT_EDITED  # Can't use None because some properties may be set to None
        self.enabled = enabled

        self._has_text = show_text
        self.display_text = get_or_make_property_display_name(property_name).upper()

        self.true_master_layout = QVBoxLayout()
        self.true_master_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.true_master_layout)

        self.display_name_label = StyledLabel(self.display_text, LabelStyle.SUBTEXT_1)
        self.true_master_layout.addWidget(self.display_name_label)
        if not show_text:
            self.display_name_label.hide()

        self.master_layout = QHBoxLayout()
        self.master_layout.setContentsMargins(0, 0, 0, 0)
        self.true_master_layout.addLayout(self.master_layout)

        self.set_enabled(enabled)


    def set_display_text(self, display_text: str | None):
        if display_text is None:
            self.display_name_label.hide()
        else:
            self.display_name_label.set_text(display_text)
            self.display_name_label.show()

    def on_value_changed(self):
        self.value_changed.emit(self.get_text())

    def set_enabled(self, enabled: bool):
        raise NotImplementedError("Subclass must implement set_enabled()")

    def get_text(self) -> tuple[str, ...]:
        raise NotImplementedError(f"Subclass {self.__class__.__name__} must implement get_text()")

    def set_value(self, value: T):
        raise NotImplementedError(f"Subclass {self.__class__.__name__} must implement set_value()")

    def get_value(self, default_value: T) -> T:
        """default_value parameter is used if the widget was never edited or if formulas are used."""
        raise NotImplementedError(f"Subclass {self.__class__.__name__} must implement get_value()")



class BooleanPropertyWidget(BasePropertyWidget):

    FORMULA_MODE_ACTIONS = [
        ('Same', lambda value: value),
        ('Invert', lambda value: not value),
        ('Off', lambda _: False),
        ('On', lambda _: True)
    ]

    def __init__(self, property_name: str, test_values: tuple[bool, ...], formula_mode: bool, initial_value: bool, enabled: bool = True, show_text: bool = True):
        super().__init__(property_name, test_values, formula_mode, initial_value, enabled, show_text)

        self.setting_widget = Switcher([name for name, _ in self.FORMULA_MODE_ACTIONS] if formula_mode else ["Off", "On"])
        self.set_value(0 if formula_mode else int(initial_value))  # If in formula mode, set value to 0 for "Same"
        self.setting_widget.index_changed.connect(self.on_value_changed)

        self.master_layout.addWidget(self.setting_widget)


    def on_value_changed(self, value: int):
        self.value = value
        super().on_value_changed()

    def set_enabled(self, enabled: bool):
        self.enabled = enabled
        self.setting_widget.set_enabled(enabled)

    def get_text(self):
        return self.FORMULA_MODE_ACTIONS[self.value][0] if self.formula_mode else ["Off", "On"][self.value]

    def set_value(self, value: int):
        self.setting_widget.set_index(value)
        self.value = value

    def get_value(self, default_value: bool) -> bool:
        return self.FORMULA_MODE_ACTIONS[self.value](default_value) if self.formula_mode else bool(self.setting_widget.get_idx())




# ----------




def get_property_widget(
    property_name: str,
    test_values: tuple[T, ...],
    formula_mode: bool,
    initial_value: T,
    enabled: bool = True,
    show_text: bool = True
) -> BasePropertyWidget[T] | None:

    property_meta_cls = brickedit.p.pmeta_registry.get(property_name, brickedit.p.UnknownPropertyMeta)
    if not isinstance(property_meta_cls, type):
        return None

    if issubclass(property_meta_cls, brickedit.p.BooleanMeta):
        return BooleanPropertyWidget(property_name, test_values, formula_mode, initial_value, enabled, show_text)

    return None

