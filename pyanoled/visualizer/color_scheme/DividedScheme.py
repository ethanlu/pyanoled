from pyanoled.event.Events import KeyEvent
from pyanoled.visualizer.color_scheme.Scheme import Scheme

from rpi_ws281x.rpi_ws281x import Color


class DividedScheme(Scheme):
    """
    divided into two colors
    """

    def getColor(self, key: KeyEvent) -> Color:
        if key.note < 60:
            return Color(255, 0, 0)
        else:
            return Color(0, 0, 255)
