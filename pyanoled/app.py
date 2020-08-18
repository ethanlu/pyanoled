from pyanoled.device.MIDIReader import MIDIReader
from pyanoled.event.EventQueue import EventQueue
from pyanoled.ui.ControlMenu import ControlMenu
from pyanoled.visualizer.LEDEngine import LEDEngine

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

        ui_thread = ControlMenu(getLogger('ui'), self._c['ui'])
        visualizer_thread = LEDEngine(getLogger('visualizer'), self._c['visualizer'], event_queue)
        midi_thread = MIDIReader(getLogger('midi'), self._c['midi'], event_queue)
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            executor.submit(ui_thread.run)
            executor.submit(visualizer_thread.run)
            executor.submit(midi_thread.run)

        self._l.info('================================== PYANOLED END ==================================')


if __name__ == "__main__":
    c = ConfigFactory.parse_file('/opt/app/conf/app.conf')
    config.dictConfig(c['log'])

    app = PyanoLED(getLogger('pyanoled'), c)
    app.run()