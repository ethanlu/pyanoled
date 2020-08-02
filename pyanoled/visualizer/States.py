from abc import ABC
from typing import Tuple


class State(ABC):
    """
    the color state of led index
    """
    def __init__(self, led_index: int, color: Tuple):
        self._led_index = led_index
        self._color = color

    @property
    def led_index(self):
        return self._led_index

    @property
    def color(self):
        return self._color


class OnState(State):
    pass

class OffState(State):
    pass

class FadingState(State):
    pass

class FlickerState(State):
    pass