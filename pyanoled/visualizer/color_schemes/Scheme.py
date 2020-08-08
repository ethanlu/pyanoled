from pyanoled.event.Events import KeyEvent

from abc import ABC, abstractmethod
from logging import Logger
from typing import Tuple

class Scheme(ABC):
    """
    base abstract class defining the interface that all color scheme subclasses needs to implement
    """

    MIN_VAL = 0
    MAX_VAL = 255

    def __init__(self, l: Logger):
        self._l = l

    @abstractmethod
    def get_color(self, key: KeyEvent) -> Tuple:
        """
        based on its color scheme design and given key event, generate the appropriate color instance
        :param key: KeyEvent instance
        :return: Color instance
        """
        pass