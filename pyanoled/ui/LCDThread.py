from pyanoled.event.EventQueue import EventQueue

from logging import Logger
from pyhocon import ConfigTree


class LCDThread(object):
    def __init__(self, l: Logger, c: ConfigTree, event_queue: EventQueue):
        self._l = l
        self._c = c
        self._event_queue = event_queue

        self._l.info('initializing lcd user interface...')

    def run(self):
        self._l.info('starting lcd user interface...')

        self._l.info('ending lcd user interface...')
