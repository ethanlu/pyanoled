from pyanoled.event.EventQueue import EventQueue
from pyanoled.event.Events import KeyEvent, PedalEvent
from pyanoled.visualizer.color_schemes.Scheme import Scheme
from pyanoled.visualizer.States import OnState, OffState, HeldState

from logging import Logger
from pyhocon import ConfigTree
from rpi_ws281x.rpi_ws281x import Color, PixelStrip
from typing import Type, Tuple

import importlib
import math


class LEDManager(object):
    def __init__(self, l: Logger, c: ConfigTree, event_queue: EventQueue):
        self._l = l
        self._c = c
        self._event_queue = event_queue
        self._pedal = False
        self._led_states = [None for i in range(88)]
        self._color_scheme = self._get_color_scheme(self._c['color_scheme'])

        self._l.info('initializing led visualizer...')

        self._pixelstrip = PixelStrip(
            self._c['count'],
            self._c['gpio_pin'],
            freq_hz=self._c['frequency'],
            dma=self._c['dma'],
            invert=self._c['invert'],
            brightness=self._c['brightness'],
            channel=self._c['channel']
        )
        self._pixelstrip.begin()

    def _get_color_scheme(self, scheme: str) -> Type[Scheme]:
        try:
            if not scheme.strip():
                scheme = 'Mono'
            name = '{s}Scheme'.format(s=scheme.strip())
            self._l.info('loading {s} color scheme...'.format(s=name))
            module = importlib.import_module('pyanoled.visualizer.color_schemes.{s}'.format(s=name))
        except ImportError as e:
            self._l.info('invalid color scheme [{s}]. using default color scheme!'.format(s=scheme))
            name = 'MonoScheme'
            module = importlib.import_module('pyanoled.visualizer.color_schemes.{s}'.format(s=name))

        clss = getattr(module, name)
        return clss(self._l)

    def _calculate_led_index(self, event: KeyEvent) -> int:
        """
        calculates the led index for the given note number
        led index starts at 0
        :param event: note key event
        :return: led index
        """
        if event.normalized_note < 3:
            # first 3 keys align with led positions 1 to 1
            return event.normalized_note
        elif 3 <= event.normalized_note < 87:
            # for keys that repeat the 12-key pattern, recalibrate the led alignment
            start = event.normalized_note - 3
            # flat offset is used for fine-tune alignment of c-key to the led
            flat_offset = (5 - int(math.floor(start / 24) * self._c['octave_alignment_drift']))
            # octave offset is for general alignment of c-key octavces to the led
            octave_offset = int(math.floor(start / 12) * 24)
            # key offset is for individual key alignment to the led relative to c-key octave
            key_offset = int(math.floor(start % 12) * 2)

            return flat_offset + octave_offset + key_offset
        else:
            # last key so use last led
            return self._c['count'] - 1

    def _adjust_brightness(self, event: KeyEvent, color: Tuple) -> Tuple:
        """
        calculates the brightness of the color based on key velocity
        :param event: note key event
        :return: brightness percentage
        """
        if self._c['force_brightness']:
            # brightness is always highest
            return color
        else:
            # velocity of 127 is high brightness and 0 is no brightness. to make led brightness difference more
            # noticeable, group the velocity into:
            # soft press : brightness reduced by 90%
            # normal press : brightness reduced by 50%
            # hard press : brightness at 100%
            if event.intensity <= self._c['keypress_soft_velocity']:
                # soft press
                return tuple(map(lambda c: int(math.floor(c * self._c['keypress_soft_multiplier'])), color))
            if self._c['keypress_soft_velocity'] < event.intensity < self._c['keypress_hard_velocity']:
                # normal press
                return tuple(map(lambda c: int(math.floor(c * self._c['keypress_normal_multiplier'])), color))
            else:
                # hard press
                return color

    def run(self):
        """
        main thread for lighting the led strip. reads events off of the event queue and performs:
        - determine led color
        - determine led intensity
        - enable/disable led
        :return:
        """
        self._l.info('starting led visualizer...')

        while True:
            for event in self._event_queue.pop_event(1000):
                self._l.info('processing {n} event : {s}'.format(n=type(event).__name__, s=str(vars(event))))

                if isinstance(event, PedalEvent):
                    self._pedal = event.is_pressed

                    if not self._pedal:
                        # pedal is lifted, so convert any led that was in held state to off state
                        for i in range(len(self._led_states)):
                            if isinstance(self._led_states[i], HeldState):
                                self._led_states[i] = OffState(self._led_states[i].led_index, self._led_states[i].color)

                if isinstance(event, KeyEvent):
                    # translate the note number to led number
                    led_index = self._calculate_led_index(event)
                    if event.is_pressed:
                        self._l.info('lighting up led {l} for note {n}'.format(l=led_index, n=event.normalized_note))
                        self._led_states[i] = OnState(led_index, self._adjust_brightness(event, self._color_scheme.getColor(event)))
                    else:
                        if self._pedal and isinstance(self._led_states[i], OnState):
                            # pedal is pressed so keep led on as held state
                            self._l.info('holding led {l}'.format(l=led_index))
                            self._led_states[i] = HeldState(led_index, self._led_states[i].color)
                        else:
                            self._l.info('shutting down led {l}'.format(l=led_index))
                            self._led_states[i] = OffState(led_index, (0, 0, 0))

            # self._pixelstrip.setPixelColor(led_index, Color(*self._adjust_brightness(event, self._color_scheme.getColor(event))))
            for i in range(len(self._led_states)):
                if self._led_states[i] is None:
                    continue
                else:
                    self._pixelstrip.setPixelColor(self._led_states[i].led_index, Color(*self._led_states[i].color))
                    if isinstance(self._led_states[i], OffState):
                        self._led_states[i] = None

            self._pixelstrip.show()

        self._l.info('ending led visualizer...')