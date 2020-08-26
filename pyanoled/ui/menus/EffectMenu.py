from pyanoled.ui.displays.Display import Display
from pyanoled.ui.menus.Menu import Menu
from pyanoled.ui.menus.SelectionItem import SelectionItem
from pyanoled.StateControl import StateControl

from logging import Logger
from typing import Optional, Type


class EffectMenu(Menu):
    def __init__(self, l: Logger, d: Type[Display], state: StateControl, parent:Optional[Type[Menu]]):
        super().__init__(l, d, state, parent)

        self._title = 'Effect'
        self._description = 'LED effect to show on key/pedal press'
        self._selections = [
            SelectionItem('Fade', 'Lights and fades over time'),
            SelectionItem('Hold', 'Lights and stays on if pedal pressed'),
            SelectionItem('Light', 'Lights on/off based on key pressed'),
        ]

    def action_confirm(self) -> Optional[Type[Menu]]:
        pass