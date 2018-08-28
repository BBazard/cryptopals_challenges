# Crack an MT19937 seed

import time
from set3.challenge21 import MT_initialize
from set3.challenge21 import MT_extractu32
import random

def get_ts():
    return int(time.time())

def get_ts_future(seconds_in_the_future):
    return int(time.time()+seconds_in_the_future)

def get_random(index, mt):
    sec = random.randint(40, 100)
    ts = get_ts_future(sec)
    index, mt = MT_initialize(ts, index, mt)
    index, mt, output = MT_extractu32(index, mt)
    return index, mt, output

if __name__ == "__main__":
    mt = [0]*624
    index = 0
    now = get_ts()
    index, mt, input = get_random(index, mt)
    for ts_tried in range(now, now+256):
        index, mt = MT_initialize(ts_tried, index, mt)
        index, mt, to_match = MT_extractu32(index, mt)
        if input == to_match:
            print("seed :", ts_tried)
