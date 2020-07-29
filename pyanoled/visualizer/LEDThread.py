from pyanoled.event.EventQueue import EventQueue

from logging import Logger
from pyhocon import ConfigTree
from rpi_ws281x.rpi_ws281x import PixelStrip
from random import randint

import time


class LEDThread(object):
    def __init__(self, l: Logger, c: ConfigTree, event_queue: EventQueue):
        self._l = l
        self._c = c
        self._event_queue = event_queue

        self._l.info('initializing led visualizer...')

        # self.pixelstrip = PixelStrip(
        #     self._c['count'],
        #     self._c['gpio_pin'],
        #     freq_hz=self._c['frequency'],
        #     dma=self._c['dma'],
        #     invert=self._c['invert'],
        #     brightness=self._c['brightness'],
        #     channel=self._c['channel']
        # )
        #self.pixelstrip.begin()

    def run(self):
        self._l.info('starting led visualizer...')

        while True:
            for e in self._event_queue.pop_event(1000):
                self._l.info('processing {n} event : {s}'.format(n=str(e.cls), s=str(vars(e))))

        self._l.info('ending led visualizer...')