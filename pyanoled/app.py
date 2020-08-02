from pyanoled.device.MIDIReader import MIDIReader
from pyanoled.event.EventQueue import EventQueue
from pyanoled.ui.LCDApp import LCDApp
from pyanoled.visualizer.LEDManager import LEDManager

from logging import config, getLogger, Logger
from pyhocon import ConfigFactory, ConfigTree

import concurrent.futures


class PyanoLED(object):
    def __init__(self, l: Logger, c: ConfigTree):
        self._l = l
        self._c = c

    def run(self):
        self._l.info('================================== PYANOLED START ==================================')

        event_queue = EventQueue()

        lcd_thread = LCDApp(self._l, self._c['lcd'], event_queue)
        led_thread = LEDManager(self._l, self._c['led'], event_queue)
        midi_thread = MIDIReader(self._l, self._c['midi'], event_queue)
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            executor.submit(lcd_thread.run)
            executor.submit(led_thread.run)
            executor.submit(midi_thread.run)

        self._l.info('================================== PYANOLED END ==================================')


if __name__ == "__main__":
    c = ConfigFactory.parse_file('/opt/app/conf/app.conf')
    config.dictConfig(c['log'])

    app = PyanoLED(getLogger('pyanoled'), c)
    app.run()