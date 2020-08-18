from abc import ABC, abstractmethod
from logging import Logger
from PIL import Image
from typing import Dict

class Display(ABC):
    """
    base abstract class defining the interface that all displays class implement
    """

    def __init__(self, l: Logger, m:Dict):
        self._l = l
        self._m = m

    @property
    @abstractmethod
    def width(self):
        pass

    @property
    @abstractmethod
    def height(self):
        pass

    @abstractmethod
    def show(self, i: Image) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass