from strip import TestStrip
import time
from animations import meteor_rain


s = TestStrip(100, auto_write=False)
while True:
    meteor_rain(s, (0xff, 0xff, 0xff), 10, 64)

