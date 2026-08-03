from PySide6.QtWidgets import QVBoxLayout, QLabel
from PySide6.QtGui import QIcon

from ui.widgets import Label, Button
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
        
        self.theme_idx = 0
        self.themes = (theme.DARK, theme.LIGHT, theme.NIGHT, theme.HIGH_CONTRAST, theme.DEV_TEST)
        button21 = Button("Change theme: Dark")
        button21.clicked.connect(self.button21_clicked)
        button21.qt_widget.setToolTip("<b>Click to change theme</b><br/>test1<br/><br/>Test2<br/><br/>Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3 Test3")
        self.button21 = button21

        
        layout2.addWidget(button21)
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
        

    def get_menu_name(self):
        return "Developer tests"

    def get_icon(self) -> base.MenuIconInfo:
        return base.MenuIconInfo(QIcon(":/assets/icons/unknown.png"), True)
