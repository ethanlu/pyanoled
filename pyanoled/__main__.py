from pyanoled import get_conf_path
from pyanoled.Configuration import Configuration
from pyanoled.device.MIDIReader import MIDIReader
from pyanoled.event.EventQueue import EventQueue
from pyanoled.State import State
from pyanoled.ui.ControlApp import ControlApp
from pyanoled.visualizer.LEDEngine import LEDEngine
from itertools import combinations
from logging import config, getLogger, Logger

import concurrent.futures
import re
import subprocess


class PyanoLED(object):
    def __init__(self, l: Logger, c: Configuration):
        self._l = l
        self._c = c
        self._port_regex = re.compile(r"^client (\d+): '(.*)'", re.IGNORECASE | re.ASCII)

    def _unlink_ports(self) -> None:
        subprocess.call('aconnect -x', shell=True)

    def _link_ports(self) -> None:
        response = subprocess.run('aconnect -l', shell=True, capture_output=True)

        ports = []
        for l in response.stdout.decode('utf-8').split('\n'):
            found = self._port_regex.findall(l)
            if found and int(found[0][0]) > 0:
                ports.append((found[0][0], found[0][1]))

        for (p1, p2) in combinations(ports, 2):
            subprocess.call(f"aconnect {p1[0]}:0 {p2[0]}:0", shell=True)
            subprocess.call(f"aconnect {p2[0]}:0 {p1[0]}:0", shell=True)

    def run(self):
        self._l.info('================================== PYANOLED START ==================================')

        event_queue = EventQueue()
        state = State()

        self._unlink_ports()
        self._link_ports()
        self._l.info('ports linked...')

        while state.is_on() or state.is_reload():
            if state.is_reload():
                self._l.info('reloading pyanoled...')
                self._unlink_ports()
                self._link_ports()
                self._l.info('ports relinked...')
                state.on()

            ui_thread = ControlApp(getLogger('ui'), self._c, state)
            visualizer_thread = LEDEngine(getLogger('visualizer'), self._c, state, event_queue)
            midi_thread = MIDIReader(getLogger('midi'), self._c, state, event_queue)
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                executor.submit(ui_thread.run)
                executor.submit(visualizer_thread.run)
                executor.submit(midi_thread.run)

        self._l.info('================================== PYANOLED END ==================================')

        if state.is_off():
            subprocess.call("sudo shutdown -h now", shell=True)

def main():
    c = Configuration(get_conf_path('app.conf'))
    config.dictConfig(c.log_configuration)

    app = PyanoLED(getLogger('pyanoled'), c)
    app.run()

if __name__ == "__main__":
    main()
