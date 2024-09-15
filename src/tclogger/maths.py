"""Math utils"""

import math


# calculate bits of integer in base
def int_bits(num, base: int = 10):
    if num == 0:
        return 0
    return int(math.log(num, base) + 1)


# get max length of dict keys
def max_key_len(d: dict):
    return max(map(len, d.keys()))
