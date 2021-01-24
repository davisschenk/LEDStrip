import time
from strip import BaseStrip, ColorTuple
from color import calculate_color_percent, wheel
import itertools
import math
import random


def rgb_fade(strip: BaseStrip, delay: int = 3):
    for color in [(255, 0, 0), (0, 255, 0), (255, 0, 0)]:
        fade_in_n_out(strip, color, delay)


def fade_in_n_out(strip: BaseStrip, color: ColorTuple, delay: int):
    for i in itertools.chain(range(256), reversed(range(256))):
        c = calculate_color_percent(color, i/256)
        strip.fill(c)
        strip.show()
        time.sleep(delay / 1000)


def strobe(strip: BaseStrip, color: ColorTuple, count: int, delay: int = 100):
    for i in range(count):
        strip.fill(color)
        strip.show()
        time.sleep(delay/1000)
        strip.fill((0, 0, 0))
        strip.show()
        time.sleep(delay/1000)


def scanner(strip: BaseStrip, color: ColorTuple, size: int, speed_delay: int = 10, return_delay: int = 50):
    for i in itertools.chain(range(strip.led_count - size - 2), reversed(range(strip.led_count - size - 2))):
        strip.fill((0, 0, 0))
        strip[i] = int(color[0]/10), int(color[1]/10), int(color[2]/10)

        for j in range(1, size+1):
            strip[i + j] = color

        strip[i+size+1] = int(color[0]/10), int(color[1]/10), int(color[2]/10)
        strip.show()
        time.sleep(speed_delay/1000)


def running_lights(strip: BaseStrip, color: ColorTuple, delay: int = 50):
    p = 0
    for j in range(strip.led_count * 2):
        p += 1
        for i in range(strip.led_count):
            strip[i] = tuple(map(lambda c: ((math.sin(i + p) * 127 + 128) / 255) * c, color))

        strip.show()
        time.sleep(delay/1000)


def color_wipe(strip: BaseStrip, color: ColorTuple, delay: int = 50):
    for i in range(strip.led_count):
        strip[i] = color
        strip.show()
        time.sleep(delay/1000)


def rainbow_cycle(strip: BaseStrip, delay: int = 20):
    for j in range(256*5):
        for i in range(strip.led_count):
            color = wheel(int((i * 256 / strip.led_count) + j) & 255)
            strip[i] = color
        strip.show()
        time.sleep(delay/1000)


def fade_to_black(strip: BaseStrip, index, value):
    old_r, old_g, old_b = strip[index]

    r = 0 if old_r <= 10 else int(old_r - (old_r * value/256))
    g = 0 if old_g <= 10 else int(old_g - (old_g * value/256))
    b = 0 if old_b <= 10 else int(old_b - (old_b * value/256))

    strip[index] = r, g, b


def meteor_rain(strip: BaseStrip, color: ColorTuple, size: int, decay: int, random_decay: bool = True, delay: int = 30):
    strip.fill((0, 0, 0))

    for i in range(strip.led_count * 2):
        for j in range(strip.led_count):
            if not random_decay or random.random() > 0.5:
                fade_to_black(strip, j, decay)

        for j in range(size):
            if strip.led_count > i-j >= 0:
                strip[i - j] = color

        strip.show()
        time.sleep(delay/1000)








