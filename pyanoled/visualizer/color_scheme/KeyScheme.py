from pyanoled.event.Events import KeyEvent
from pyanoled.visualizer.color_scheme.Scheme import Scheme

from rpi_ws281x.rpi_ws281x import Color


class KeyScheme(Scheme):
    """
    two colors mapped to black and white keys
    """

    def getColor(self, key: KeyEvent) -> Color:
        # normalize the note so lowest key starts at 0
        normalized_note = key.note - key.MIN_NOTE

        if normalized_note < 3:
            # first 3 keys sequenced as:
            # white-black-white
            if normalized_note == 1:
                return self._getBlackKeyColor()
            else:
                return self._getWhiteKeyColor()
        elif 3 <= normalized_note < 87:
            # keys after 3rd and before 88th are sequenced as 12-keys repeated as:
            # white-black-white-black-white white-black-white-black-white-black-white
            r = (normalized_note - 3) % 12
            if (r <= 4 and r % 2 == 1) or (r > 4 and r % 2 == 0):
                return self._getBlackKeyColor()
            else:
                return self._getWhiteKeyColor()
        else:
            # last key is white
            return self._getWhiteKeyColor()

    def _getWhiteKeyColor(self):
        return Color(0, 0, 128)

    def _getBlackKeyColor(self):
        return Color(255, 215, 0)
