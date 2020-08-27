from pyanoled.Configuration import Configuration
from pyanoled.device.MIDIReader import MIDIReader
from pyanoled.event.EventQueue import EventQueue
from pyanoled.State import State
from pyanoled.ui.ControlApp import ControlApp
from pyanoled.visualizer.LEDEngine import LEDEngine

from logging import config, getLogger, Logger
from subprocess import call

import concurrent.futures


class PyanoLED(object):
    def __init__(self, l: Logger, c: Configuration):
        self._l = l
        self._c = c

    def run(self):
        self._l.info('================================== PYANOLED START ==================================')

        event_queue = EventQueue()
        state = State()

        while state.is_on() or state.is_reload():
            ui_thread = ControlApp(getLogger('ui'), self._c, state)
            visualizer_thread = LEDEngine(getLogger('visualizer'), self._c, state, event_queue)
            midi_thread = MIDIReader(getLogger('midi'), self._c, state, event_queue)
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                executor.submit(ui_thread.run)
                executor.submit(visualizer_thread.run)
                executor.submit(midi_thread.run)

        self._l.info('================================== PYANOLED END ==================================')

        if state.is_off():
            call("sudo shutdown -h now", shell=True)


if __name__ == "__main__":
    c = Configuration('/opt/app/conf/app.conf')
    config.dictConfig(c.log_configuration)

    app = PyanoLED(getLogger('pyanoled'), c)
    app.run()