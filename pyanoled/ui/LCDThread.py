from pyanoled.event.EventQueue import EventQueue

from random import randint
from logging import Logger
from pyhocon import ConfigTree

import time


class LCDThread(object):
    def __init__(self, l: Logger, c: ConfigTree, event_queue: EventQueue):
        self._l = l
        self._c = c
        self._event_queue = event_queue

        self._l.info('initializing lcd user interface...')

    def run(self):
        self._l.info('starting lcd user interface...')
        for i in range(10):
            self._l.info('lcd screen #{i}'.format(i=str(i)))
            time.sleep(randint(1, 10000)/1000)
        self._l.info('ending lcd user interface...')
