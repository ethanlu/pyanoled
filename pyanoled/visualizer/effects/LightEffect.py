from pyanoled.visualizer.effects.Effect import Effect

from rpi_ws281x.rpi_ws281x import Color

class LightEffect(Effect):
    """
    default light effect that lights up led when key is pressed and shuts led off when key is lifted
    """

    def pedal_on(self) -> None:
        pass

    def pedal_off(self) -> None:
        pass

    def key_on(self, led_index: int, color: Color) -> None:
        self._l.info('lighting up led {l}'.format(l=led_index))
        self._pixelstrip.setPixelColor(led_index, color)

    def key_off(self, led_index: int, color: Color) -> None:
        self._l.info('shutting down led {l}'.format(l=led_index))
        self._pixelstrip.setPixelColor(led_index, color)
