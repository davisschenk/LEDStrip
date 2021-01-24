from abc import ABC, abstractmethod
from typing import Union
import time
import warnings
try:
    from matplotlib import pyplot as plt
    import numpy as np
except ImportError:
    warnings.warn("Testing is not supported on this device")

try:
    import board
    import neopixel
except (ImportError, NotImplementedError):
    warnings.warn("Neopixel is not supported on this device")


ColorTuple = tuple[int, int, int]


class BaseStrip(ABC):
    """
    Abstract LED strip control interface

    Parameters
    ___________

    led_count: int
        The number of leds in the strip

    auto_write: bool
        Whether or not leds should be auto-updated
    """

    def __init__(self, led_count: int, auto_write: bool = True):
        self.led_count = led_count
        self.auto_write = auto_write

        self._state = [(0, 0, 0) for i in range(led_count)]

    @abstractmethod
    def get_pixel(self, index: Union[int, slice]) -> ColorTuple:
        raise NotImplemented

    def __getitem__(self, index: Union[int, slice]) -> ColorTuple:
        return self.get_pixel(index)

    @abstractmethod
    def set_pixel(self, index: int, color: ColorTuple):
        raise NotImplemented

    def __setitem__(self, index: int, color: ColorTuple):
        self.set_pixel(index, color)

    @abstractmethod
    def set_pixel_slice(self, pixels: slice, color: ColorTuple, delay=0):
        raise NotImplemented

    @abstractmethod
    def show(self):
        raise NotImplemented

    @abstractmethod
    def fill(self, color: ColorTuple):
        raise NotImplemented


class TestStrip(BaseStrip):
    """
    A LED strip interface which can be used to visualize the colors which will be displayed on the strip

    Parameters
    ___________

    led_count: int
        The number of leds in the strip

    auto_write: bool
        Whether or not to auto-update plot
    """

    def __init__(self, led_count: int, auto_write: bool = True):
        super().__init__(led_count)
        self.auto_write = auto_write
        self.image_arr = np.zeros((1, led_count, 3), dtype=np.uint8)

        plt.ion()
        self.fig, self.ax = plt.subplots()
        plt.gca().axes.get_yaxis().set_visible(False)

        self.axim = self.ax.imshow(self.image_arr)

    def plot_state(self):
        self.axim.set_data(self.image_arr)
        self.fig.canvas.flush_events()

    def get_pixel(self, index: Union[int, slice]) -> ColorTuple:
        return self._state[index]

    def set_pixel(self, index: int, color: ColorTuple):
        self._state[index] = color
        self.image_arr[0, index] = color

        if self.auto_write:
            self.plot_state()

    def show(self):
        self.plot_state()

    def set_pixel_slice(self, pixels: slice, color: ColorTuple, delay=0):
        for pixel in range(pixels.start, pixels.stop, pixels.step):
            self.set_pixel(pixel, color)
            time.sleep(delay)

    def fill(self, color: ColorTuple):
        for pixel in range(self.led_count):
            self._state[pixel] = color
            self.image_arr[0, pixel] = color

        if self.auto_write:
            self.plot_state()


class NeopixelStrip(BaseStrip):
    """
    A LED strip interface which can be used with Neopixel led strips

    Parameters
    ___________

    led_count: int
        The number of leds in the strip

    board_type
        The board which is passed to Neopixel

    auto_write: bool
        Whether or not to auto-update plot

    kwargs:
        Kwargs are passed to neopixel.Neopixel
    """
    def __init__(self, led_count: int, board_type, auto_write: bool = True, **kwargs):
        super().__init__(led_count)
        self.led_count = led_count
        self.neopixel = neopixel.Neopixel(board_type, led_count, auto_write=auto_write, **kwargs)

    def set_pixel(self, index: int, color: ColorTuple):
        self.neopixel[index] = color
        self._state = color

    def get_pixel(self, index: Union[int, slice]) -> ColorTuple:
        return self._state[index]

    def set_pixel_slice(self, pixels: slice, color: ColorTuple, delay=0):
        for pixel in range(pixels.start, pixels.stop, pixels.step):
            self.set_pixel(pixel, color)
            time.sleep(delay)

    def show(self):
        self.neopixel.show()

    def fill(self, color: ColorTuple):
        self.neopixel.fill(color)
