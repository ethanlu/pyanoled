from pyanoled.event.Events import KeyEvent
from pyanoled.visualizer.color_scheme.Scheme import Scheme

from rpi_ws281x.rpi_ws281x import Color
from random import randint


class ChaosScheme(Scheme):
    """
    random colors every time
    """

    def getColor(self, key: KeyEvent) -> Color:
        return Color(randint(0, 255),randint(0, 255),randint(0, 255))