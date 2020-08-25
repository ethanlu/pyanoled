from pyanoled.ui.displays.Display import Display
from pyanoled.StateControl import StateControl

from logging import Logger
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, Type


structure = {
    'label': 'PyanoLED',
    'description': '',
    'type': 'select',
    'options': (
        {
            'label': 'Color Scheme',
            'description': 'LED color to show on key press',
            'type': 'select',
            'options': (
                {
                    'label': 'Chaos',
                    'desription': 'Random color everytime',
                    'type': 'value'
                },
                {
                    'label': 'Divided',
                    'description': '2 colors split on middle C',
                    'type': 'value'
                },
                {
                    'label': 'Key',
                    'description': '2 colors for key color',
                    'type': 'value'
                },
                {
                    'label': 'Mono',
                    'description': '1 color for all',
                    'type': 'value'
                },
            )
        },
        {
            'label': 'Effect',
            'description': 'LED effect to show on key/pedal press',
            'options': (
                {
                    'label': 'Fade',
                    'description': 'Lights and fades over time',
                    'type': 'value'
                },
                {
                    'label': 'Hold',
                    'description': 'Lights and stays on if pedal pressed',
                    'type': 'value'
                },
                {
                    'label': 'Light',
                    'description': 'Lights on/off based on key pressed',
                    'type': 'value'
                }
            )
        },
        {
            'label': 'Shutdown',
            'description': 'Shutdown PyanoLED',
            'type': 'value'
        }
    )
}

DEFAULT_PATH = 'PyanoLED'
PATH_DELIMITER = '>'

class Menu(object):
    def __init__(self, l: Logger, d: Type[Display], state: StateControl):
        self._l = l
        self._display = d
        self._state = state
        self._path = DEFAULT_PATH
        self._position = 0
        self._image = None

    def _get_menu_items(self) -> Tuple:
        parts = self._path.split(PATH_DELIMITER)
        current = structure
        for p in parts:
            if current['label'] == p:
                current = current['options']
            else:
                raise Exception('Invalid path part : {s}'.format(s=p))
        return current

    def _multiline_split(self, s: str, n: int = 2) -> Tuple:
        """
        splits s into max of n lines based on display's character width
        :param s: string to split
        :param n: max number of lines
        :return:
        """
        lines = []
        t = ''
        for p in s.split(' '):
            if len(t + ' ' +p) < self._display.character_width:
                # can fit in current line
                t += ' ' + p
            else:
                # need new line
                if len(lines) < n - 1:
                    # max lines not reached
                    lines.append(t.strip())
                    t = p
                else:
                    # max line reached...truncate
                    t = (t + ' '  + p)[:(self._display.character_width - 5)] + '...'
                    break

        if t and len(lines) < n:
            lines.append(t.strip())

        return lines

    def up(self) -> None:
        if self._position == 0:
            # wrap around to last item
            self._position = len(self._get_menu_items()) - 1
        else:
            self._position -= 1

    def down(self) -> None:
        if self._position == len(self._get_menu_items()) - 1:
            self._position = 0
        else:
            self._position += 1

    def ok(self) -> None:
        if self._path == DEFAULT_PATH and self._position == 2:
            self._state.off()

    def show(self) -> None:
        """
        draw menu based on current path and selection
        :return:
        """
        self._image = Image.new('RGB', (self._display.height, self._display.width), (0, 0, 0))
        draw = ImageDraw.Draw(self._image)

        # draw path
        y = 1
        draw.text((1, y), self._path.split(PATH_DELIMITER)[-1], fill=(255, 255, 255))
        y += self._display.character_height
        draw.line([(0, y), (self._display.width, y)], fill=(255, 255, 255), width = 1)
        y += 1

        # draw menu items
        items = self._get_menu_items()
        footnote = ''
        for i, v in enumerate(items):
            # only show times that fit
            if y < (self._display.height - self._display.character_height*3):
                # has room still
                if self._position == i:
                    footnote = v['description'] or ''
                    draw.rectangle([(0, y), (self._display.width, y + self._display.character_height)], fill=(255, 0, 0))
                draw.text((1, y), v['label'], fill=(255, 255, 255))
                y += self._display.character_height

        # draw footnote
        y = self._display.height - self._display.character_height*2 - 1
        draw.line([(0, y), (self._display.width, y)], fill=(255, 255, 255), width=1)
        y += 1
        for l in self._multiline_split(footnote, 2):
            draw.text((1, y), l, fill=(255, 255, 255))
            y += self._display.character_height

        self._display.show(self._image)
