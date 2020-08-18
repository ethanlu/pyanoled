from pyanoled.ui.display.Display import Display
from pyanoled.ui.display import LCD_1in44, LCD_Config

from PIL import Image


class Waveshare144Display(Display):
    """
    https://www.waveshare.com/wiki/File:1.44inch-LCD-HAT-All-Code.7z
    """
    def __init__(self):
        self._lcd = LCD_1in44.LCD()
        self._lcd_scandir = LCD_1in44.SCAN_DIR_DFT
        self._lcd.LCD_Init(self._lcd_scandir)
        self._lcd.LCD_Clear()

    @property
    def width(self):
        return 128

    @property
    def height(self):
        return 128

    def show(self, i: Image) -> None:
        self._lcd.LCD_ShowImage(i, 0, 0)

    def clear(self) -> None:
        self._lcd.LCD_Clear()
