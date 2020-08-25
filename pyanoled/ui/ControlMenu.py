from pyanoled.StateControl import StateControl
from pyanoled.ui.displays.Display import Display
from pyanoled.ui.Menu import Menu

from logging import Logger
from PIL import Image, ImageDraw
from pyhocon import ConfigTree
from typing import Type

import importlib
import RPi.GPIO as GPIO
import time


DEFAULT_DISPLAY = 'Waveshare144'

class ControlMenu(object):
    def __init__(self, l: Logger, c: ConfigTree, state: StateControl):
        self._l = l
        self._c = c
        self._state = state

        self._l.info('initializing displays...')
        self._display = self._get_display(c['display'])
        self._menu = Menu(self._l, self._display, self._state)

        # key press to channel #
        self._dpad_up = 6
        self._dpad_down = 19
        self._dpad_left = 5
        self._dpad_right = 26
        self._dpad_press = 13
        self._button_a = 21
        self._button_b = 20
        self._button_c = 16

        # init gpio
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._dpad_up, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self._dpad_down, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self._dpad_left, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self._dpad_right, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self._dpad_press, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self._button_a, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self._button_b, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self._button_c, GPIO.IN, GPIO.PUD_UP)
        GPIO.add_event_detect(self._dpad_up, GPIO.RISING)
        GPIO.add_event_detect(self._dpad_down, GPIO.RISING)
        GPIO.add_event_detect(self._dpad_left, GPIO.RISING)
        GPIO.add_event_detect(self._dpad_right, GPIO.RISING)
        GPIO.add_event_detect(self._dpad_press, GPIO.RISING)
        GPIO.add_event_detect(self._button_a, GPIO.RISING)
        GPIO.add_event_detect(self._button_b, GPIO.RISING)
        GPIO.add_event_detect(self._button_c, GPIO.RISING)

    def _get_display(self, display: str) -> Type[Display]:
        try:
            if not display.strip():
                name = DEFAULT_DISPLAY
            name = '{s}Display'.format(s=display.strip())
            self._l.info('loading {s} displays...'.format(s=name))
            module = importlib.import_module('pyanoled.ui.displays.{s}'.format(s=name))
        except ImportError as e:
            self._l.warning('invalid displays {s}. using default displays!'.format(s=name))
            name = '{s}Display'.format(s=DEFAULT_DISPLAY)
            module = importlib.import_module('pyanoled.ui.displays.{s}'.format(s=name))

        clss = getattr(module, name)
        return clss(self._l)

    def run(self) -> None:
        self._l.info('starting control menu...')

        try:
            image = Image.new('RGB', (self._display.height, self._display.width), (0, 0, 0))
            draw = ImageDraw.Draw(image)
            draw.text(
                (
                    round(self._display.width/2) - 24,
                    round(self._display.height/2) - round(self._display.character_height/2)
                ),
                'PYANOLED', fill=(255, 255, 255))
            self._display.show(image)
            time.sleep(2)

            self._menu.show()

            while self._state.is_on():
                if GPIO.event_detected(self._dpad_up):
                    self._l.debug('dpad up pressed')
                    self._menu.up()
                    self._menu.show()
                if GPIO.event_detected(self._dpad_down):
                    self._l.debug('dpad down pressed')
                    self._menu.down()
                    self._menu.show()
                if GPIO.event_detected(self._dpad_left):
                    self._l.debug('dpad left pressed')
                    pass
                if GPIO.event_detected(self._dpad_right):
                    self._l.debug('dpad right pressed')
                    pass
                if GPIO.event_detected(self._dpad_press):
                    self._l.debug('dpad pressed')
                    pass
                if GPIO.event_detected(self._button_a):
                    self._l.debug('button a pressed')
                    self._menu.ok()
                    self._menu.show()
                if GPIO.event_detected(self._button_b):
                    self._l.debug('button b pressed')
                    pass
                if GPIO.event_detected(self._button_c):
                    self._l.debug('button c pressed')
                    pass

                time.sleep(.01)
        except:
            self._l.exception('control menu error!')
            self._state.error()

        self._l.info('ending control menu...')
        self._display.clear()
        GPIO.cleanup()
