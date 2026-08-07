from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtGui import QIcon, QRegularExpressionValidator

from ui.widgets import Label, Button, Slider, ComboBox, LineEdit
import ui.theme as theme
from ui.models import TooltipContents

from menus import base
from ..shared_widgets import TabMenu


class DeveloperTestMenu(base.BaseMenu):

    def __init__(self, mw):
        super().__init__(mw)

        layout1 = QVBoxLayout()
        label11 = QLabel("First menu")
        layout1.addWidget(label11)
        label12 = QLabel("Second menu")
        layout1.addWidget(label12)
        layout1.addStretch()

        layout2 = QVBoxLayout()
        label21 = Label("Hello, World")
        layout2.addWidget(label21)
        label22 = Label("Hello, World 2")
        label22.set_tooltip(TooltipContents("hello", "world world world world"))
        layout2.addWidget(label22)

        themes_layout = QHBoxLayout()
        layout2.addLayout(themes_layout)

        self.theme_idx = 0
        self.themes = theme.theme_manager.themes
        button21 = Button("Change theme: Dark")
        button21.clicked.connect(self.button21_clicked)
        button21.qt_widget.setToolTip("<b>Click to change theme</b><br/>test1<br/><br/>Test2<br/><br/>Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3")
        self.button21 = button21
        themes_layout.addWidget(button21)

        QICON_1 = QIcon(":/assets/icons/HomeIcon.png")
        QICON_2 = QIcon(":/assets/icons/GradientIcon.png")
        combobox21 = ComboBox()
        combobox21.add_item("World", QICON_1)
        combobox21.add_item("World 2", QICON_2)
        themes_layout.addWidget(combobox21)

        slider21 = Slider(range(0, 50, 5), 15)
        slider21.set_text("Value is 15", 80)
        slider21.value_changed.connect(self.update_slider21)
        self.slider21 = slider21
        layout2.addWidget(slider21)


        lineedit21 = LineEdit('1A2B3C4D')
        validator = QRegularExpressionValidator("^[0-9A-Fa-f]{8}$")
        lineedit21.set_validator(validator)
        layout2.addWidget(lineedit21)


        layout2.addStretch()

        self.tab_menu = TabMenu()
        self.tab_menu.add_menu(0, "Hello", layout1)
        self.tab_menu.add_menu(1, "World", layout2)
        self.master_layout.addWidget(self.tab_menu)


        self.master_layout.addStretch()

    def button21_clicked(self):
        self.theme_idx = (self.theme_idx + 1) % len(self.themes)
        new_theme = self.themes[self.theme_idx]
        theme.theme_manager.set_theme(new_theme)
        self.button21.set_text(f"Change theme: {new_theme.display_name}")
        
    def update_slider21(self):
        self.slider21.set_text(f"Value is {self.slider21.get_value()}", 80)

    def get_menu_name(self):
        return "Developer tests"

    def get_icon(self) -> base.MenuIconInfo:
        return base.MenuIconInfo(QIcon(":/assets/icons/unknown.png"), True)
