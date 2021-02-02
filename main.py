from strip import TestStrip
import time
from animations import *

s = TestStrip(30, auto_write=False)

while True:
    police_lights(s, 20)
