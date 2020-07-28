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
    def note(self):
        return self._msg.note

    @property
    def value(self):
        return self._msg.value

    @property
    def velocity(self):
        return self._msg.velocity
