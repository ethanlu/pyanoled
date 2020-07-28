from pyanoled.event.Event import Event

from collections import deque
from threading import Lock
from typing import List


class EventQueue(object):
    """
    shared queue used to store events written by device threads and read by visualizer thread
    """
    def __init__(self):
        self._events = deque([])
        self._lock = Lock()

    def pop_event(self, n: int = 1) -> List[Event]:
        """
        pops off n Events from the event queue and returns in a list
        :param n: number of events to remove from the event queue, if less than n events exist then all events removed
        :return: List[Event]
        """
        # lock the event queue to ensure nothing is writing to it while reading
        with self._lock:
            events = [self._events.popleft() for i in range(max(n, len(self._events)))]

        return events

    def push_event(self, events: List[Event]) -> bool:
        """
        pushes given list of Events objects to event queue
        :param events:
        :return:
        """
        # lock the event queue to ensure nothing is reading from it while writing
        with self._lock:
            self._events.extend(events)

        return True