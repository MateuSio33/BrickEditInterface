from collections.abc import Callable
from PySide6.QtCore import QObject, Property, QPropertyAnimation, QEasingCurve


class PulseAnimation(QObject):
    """
    Generic looping 0 -> 1 -> 0 animation.

    callback(value) is called whenever the animation changes.
    """

    def __init__(
        self,
        callback: Callable[[float], None],
        duration: int = 900,
        parent=None,
    ):
        super().__init__(parent)

        self._value = 0.0
        self._active = False
        self._callback = callback

        self._anim = QPropertyAnimation(self, b"value")
        self._anim.setDuration(duration)
        self._anim.setStartValue(0.0)
        self._anim.setKeyValueAt(0.5, 1.0)
        self._anim.setEndValue(0.0)
        self._anim.setLoopCount(-1)
        self._anim.setEasingCurve(QEasingCurve.InOutSine)

    @Property(float)
    def value(self):
        return self._value

    @value.setter
    def value(self, value: float):
        self._value = value
        self._callback(value)

    def start(self):
        if self._active:
            return

        self._active = True
        self._anim.start()

    def stop(self):
        if not self._active:
            return

        self._active = False
        self._anim.stop()

        self.value = 0.0

    def is_active(self) -> bool:
        return self._active

    def current_value(self) -> float:
        return self._value
