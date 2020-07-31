from pyanoled.event.Events import KeyEvent, PedalEvent
from pyanoled.event.EventQueue import EventQueue

from logging import Logger
from pyhocon import ConfigTree

import mido


class MIDIThread(object):
    def __init__(self, l: Logger, c: ConfigTree, event_queue: EventQueue):
        self._l = l
        self._c = c
        self._event_queue = event_queue

        self._l.info('initializing midi listener...')

        # open input port based on information from config
        self._input_port = mido.open_input([s for s in mido.get_input_names() if s.startswith(self._c['input_port_prefix'])][0])

    def run(self):
        self._l.info('starting midi listener...')

        while True:
            # listen on input port for messages and extract out the pertinent ones
            pending = []
            for m in self._input_port.iter_pending():
                if m.type == 'note_on' and KeyEvent.MIN_NOTE <= m.note <= KeyEvent.MAX_NOTE:
                    self._l.info('key event : {s}'.format(s=str(vars(m))))
                    pending.append(KeyEvent(m))
                elif m.type == 'control_change' and m.control == PedalEvent.PEDAL_VAL:
                    self._l.info('pedal event : {s}'.format(s=str(vars(m))))
                    pending.append(PedalEvent(m))

            # append events to queue...rinse and repeat
            self._event_queue.push_event(pending)
        self._l.info('ending midi listener...')