from pyanoled.event.Events import KeyEvent
from pyanoled.visualizer.color_scheme.Scheme import Scheme

from rpi_ws281x.rpi_ws281x import Color


class MonoScheme(Scheme):
    """
    one color for all keys
    """

    def getColor(self, key: KeyEvent) -> Color:
        return Color(255, 255, 255)