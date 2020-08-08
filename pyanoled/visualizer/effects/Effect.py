from abc import ABC, abstractmethod
from logging import Logger
from rpi_ws281x.rpi_ws281x import Color, PixelStrip

class Effect(ABC):
    """
    base abstract class defining the interface that all effect scheme subclasses needs to implement
    """

    def __init__(self, l: Logger):
        self._l = l
        self._pixelstrip = None

    def set_pixelstrip(self, pixel_strip: PixelStrip):
        self._pixelstrip = pixel_strip

    @abstractmethod
    def pedal_on(self) -> None:
        """
        method invoked when pedal is pressed
        :param key: KeyEvent instance
        :return:
        """
        pass

    @abstractmethod
    def pedal_off(self) -> None:
        """
        method invoked when pedal is lifted
        :param key: KeyEvent instance
        :return:
        """
        pass

    @abstractmethod
    def key_on(self, led_index: int, color: Color) -> None:
        """
        method invoked when key is pressed
        :param key: KeyEvent instance
        :return:
        """
        pass

    @abstractmethod
    def key_off(self, led_index: int, color: Color) -> None:
        """
        method invoked when key is lifted
        :param key: KeyEvent instance
        :return:
        """
        pass
