from mido.messages import Message

class Event(object):
    """
    wrapper for mido Message objects coming from midi port
    """
    def __init__(self, msg: Message):
        self._msg = msg

    @property
    def channel(self):
        return self._msg.channel

    @property
    def type(self):
        return self._msg.type

    @property
    def time(self):
        return self._msg.time


class KeyEvent(Event):
    """
    event representing key presses
    {'type': 'note_on', 'time': 0, 'note': 60, 'velocity': 63, 'channel': 0}
    {'type': 'note_on', 'time': 0, 'note': 64, 'velocity': 0, 'channel': 0}
    """
    @property
    def note(self):
        # note 60 is middle c
        return self._msg.note

    def intensity(self):
        # velocity measures how hard the key was pressed, 0 means not pressed
        return self._msg.velocity

    @property
    def is_pressed(self):
        return self._msg.velocity > 0


class PedalEvent(Event):
    """
    event representing dampner/soft pedal press
        {'type': 'control_change', 'time': 0, 'control': 64, 'value': 127, 'channel': 0}
        {'type': 'control_change', 'time': 0, 'control': 64, 'value': 0, 'channel': 0}
    """
    @property
    def is_pressed(self):
        # value of 0 is not pressed
        return self._msg.value > 0
