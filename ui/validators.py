from PySide6.QtGui import QRegularExpressionValidator

HEX_4COLOR_VALIDATOR = QRegularExpressionValidator(r"^[a-fA-F0-9]{8}$")
