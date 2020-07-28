from pyanoled.event.EventQueue import EventQueue

from logging import Logger
from pyhocon import ConfigTree
from random import randint

import time


class MIDIThread(object):
    def __init__(self, l: Logger, c: ConfigTree, event_queue: EventQueue):
        self._l = l
        self._c = c
        self._event_queue = event_queue

        self._l.info('initializing midi listener...')

    def run(self):
        self._l.info('starting midi listener...')
        for i in range(10):
            self._l.info('midi listener #{i}'.format(i=str(i)))
            time.sleep(randint(1, 10000)/1000)
        self._l.info('ending midi listener...')