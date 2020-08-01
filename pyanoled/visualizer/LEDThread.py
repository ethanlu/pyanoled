from pyanoled.event.EventQueue import EventQueue
from pyanoled.event.Events import KeyEvent
from pyanoled.visualizer.color_scheme.Scheme import Scheme

from logging import Logger
from pyhocon import ConfigTree
from rpi_ws281x.rpi_ws281x import Color, PixelStrip
from typing import Type

import importlib


class LEDThread(object):
    def __init__(self, l: Logger, c: ConfigTree, event_queue: EventQueue):
        self._l = l
        self._c = c
        self._event_queue = event_queue
        self._color_scheme = self._get_color_scheme(self._c['color_scheme'])

        self._l.info('initializing led visualizer...')

        self._pixelstrip = PixelStrip(
            self._c['count'],
            self._c['gpio_pin'],
            freq_hz=self._c['frequency'],
            dma=self._c['dma'],
            invert=self._c['invert'],
            brightness=self._c['brightness'],
            channel=self._c['channel']
        )
        self._pixelstrip.begin()

    def _get_color_scheme(self, scheme: str) -> Type[Scheme]:
        try:
            if not scheme.strip():
                scheme = 'Mono'
            name = '{s}Scheme'.format(s=scheme.strip())
            self._l.info('loading {s} color scheme...'.format(s=name))
            module = importlib.import_module('pyanoled.visualizer.color_scheme.{s}'.format(s=name))
        except ImportError as e:
            self._l.info('invalid color scheme [{s}]. using default color scheme!'.format(s=scheme))
            name = 'MonoScheme'
            module = importlib.import_module('pyanoled.visualizer.color_scheme.{s}'.format(s=name))

        clss = getattr(module, name)
        return clss(self._l)

    def _calculate_led_index(self, note: int) -> int:
        """
        calculates the led index for the given note number
        :param note: note number
        :return: led index
        """
        normalized_note = note - KeyEvent.MIN_NOTE
        if 0 < normalized_note < 88:
            return int(round((self._c['count'] / 88) * normalized_note))
        else:
            return 0

    def run(self):
        """
        main thread for lighting the led strip. reads events off of the event queue and performs:
        - determine led color
        - determine led intensity
        - enable/disable led
        :return:
        """
        self._l.info('starting led visualizer...')

        while True:
            for event in self._event_queue.pop_event(1000):
                self._l.info('processing {n} event : {s}'.format(n=str(event.cls), s=str(vars(event))))

                if isinstance(event, 'KeyEvent'):
                    # translate the note number to led number
                    led_number = self._calculate_led_index(event.note)
                    if event.is_pressed():
                        # light it up!
                        self._pixelstrip.setPixelColor(led_number, self._color_scheme.getColor(event))
                    else:
                        # shut it down!
                        self._pixelstrip.setPixelColor(led_number, Color(0, 0, 0))

        self._l.info('ending led visualizer...')