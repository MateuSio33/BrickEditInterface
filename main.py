"""BrickEdit Interface - Main entry point."""

from sys import argv, exit as sys_exit
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon, QFontDatabase, QFont
import resources_rc  # your compiled Qt resources
from systems.log import setup_logging

from mainwindow import BrickEditInterface

def main():
    setup_logging()

    app = QApplication(argv)
    # app.setStyle("Fusion")

    font_id = QFontDatabase.addApplicationFont(":/assets/fonts/SofiaSansCondensed-VariableFont_wght.ttf")
    QFontDatabase.addApplicationFont(":/assets/fonts/SofiaSansCondensed-Italic-VariableFont_wght.ttf")
    # QFontDatabase.addApplicationFont(":/assets/fonts/SofiaSansCondensed-VariableFont_wght.ttf")
    family = QFontDatabase.applicationFontFamilies(font_id)[0]
    app.setFont(QFont(family))

    # Title bar icon (cross-platform)
    bei_icon = QIcon(":/assets/icons/brickeditinterface.ico")
    app.setWindowIcon(bei_icon)

    window = BrickEditInterface()
    window.setWindowIcon(bei_icon)

    window.show()
    sys_exit(app.exec())


if __name__ == "__main__":
    main()
