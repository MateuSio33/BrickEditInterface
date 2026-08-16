from PySide6.QtGui import QRegularExpressionValidator

HEX_4COLOR_VALIDATOR = QRegularExpressionValidator(r"^[a-fA-F0-9]{8}$")
BINARY_HEX_VALIDATOR = QRegularExpressionValidator(r"^(?:[0-9A-Fa-f]{2}(?: ?[0-9A-Fa-f]{2})*)$")
