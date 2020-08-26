from pyanoled.ui.displays.Display import Display
from pyanoled.ui.menus.Menu import Menu
from pyanoled.ui.menus.ColorSchemeMenu import ColorSchemeMenu
from pyanoled.ui.menus.EffectMenu import EffectMenu
from pyanoled.ui.menus.SelectionItem import SelectionItem
from pyanoled.StateControl import StateControl

from logging import Logger
from typing import Optional, Type


class MainMenu(Menu):
    def __init__(self, l: Logger, d: Type[Display], state: StateControl, parent:Optional[Type[Menu]]):
        super().__init__(l, d, state, parent)

        self._title = 'PyanoLED'
        self._description = ''
        self._selections = (
            ColorSchemeMenu(self._l, self._display, self._state, self),
            EffectMenu(self._l, self._display, self._state, self),
            SelectionItem('Power', 'Power options for PyanoLED'),
        )

    def action_confirm(self) -> Optional[Type[Menu]]:
        item = self._get_selected()
        if isinstance(item, Menu):
            return item
        elif item.title == 'Power':
            self._state.off()
            return None
        else:
            raise Exception('Invalid item : {i}'.format(i=str(item)))