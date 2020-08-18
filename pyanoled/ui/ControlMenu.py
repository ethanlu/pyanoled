from pyanoled.ui.display.Display import Display
from pyanoled.ui.menu import menu

from logging import Logger
from PIL import Image, ImageDraw, ImageFont
from pyhocon import ConfigTree
from typing import Type

import importlib


class ControlMenu(object):
    def __init__(self, l: Logger, c: ConfigTree):
        self._l = l
        self._c = c

        self._l.info('initializing display...')
        self._display = self._get_display(c['display'])

    def _get_display(self, display: str) -> Type[Display]:
        try:
            if not display.strip():
                scheme = 'Waveshare144'
            name = '{s}Display'.format(s=display.strip())
            self._l.info('loading {s} display...'.format(s=name))
            module = importlib.import_module('pyanoled.ui.display.{s}'.format(s=name))
        except ImportError as e:
            self._l.warning('invalid display [{s}]. using default display!'.format(s=scheme))
            name = 'Waveshare144'
            module = importlib.import_module('pyanoled.ui.display.{s}'.format(s=name))

        clss = getattr(module, name)
        return clss(self._l, menu)

    def run(self):
        self._l.info('starting control menu interface...')

        self._l.info('ending control menu interface...')
