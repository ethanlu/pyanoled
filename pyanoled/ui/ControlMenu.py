from pyanoled.ui.displays.Display import Display
from pyanoled.ui.Menu import Menu

from logging import Logger
from PIL import Image, ImageDraw
from pyhocon import ConfigTree
from typing import Type

import importlib
import time


DEFAULT_DISPLAY = 'Waveshare144'

class ControlMenu(object):
    def __init__(self, l: Logger, c: ConfigTree):
        self._l = l
        self._c = c

        self._l.info('initializing displays...')
        self._display = self._get_display(c['display'])
        self._menu = Menu(self._l, self._display)

    def _get_display(self, display: str) -> Type[Display]:
        try:
            if not display.strip():
                name = DEFAULT_DISPLAY
            name = '{s}Display'.format(s=display.strip())
            self._l.info('loading {s} displays...'.format(s=name))
            module = importlib.import_module('pyanoled.ui.displays.{s}'.format(s=name))
        except ImportError as e:
            self._l.warning('invalid displays {s}. using default displays!'.format(s=name))
            name = '{s}Display'.format(s=DEFAULT_DISPLAY)
            module = importlib.import_module('pyanoled.ui.displays.{s}'.format(s=name))

        clss = getattr(module, name)
        return clss(self._l)

    def run(self) -> None:
        self._l.info('starting control menu...')
        image = Image.new('RGB', (self._display.height, self._display.width), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.text((40, 60), 'PYANOLED', fill=(255, 255, 255))
        self._display.show(image)
        time.sleep(3)

        self._menu.show()

        while True:
            time.sleep(60)

        self._l.info('ending control menu...')
        self._display.clear()
