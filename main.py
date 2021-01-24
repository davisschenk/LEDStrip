from strip import TestStrip
import time
from animations import snake


s = TestStrip(50, auto_write=False)

snake(s, (0, 255, 0), (255, 0, 0), 10)
