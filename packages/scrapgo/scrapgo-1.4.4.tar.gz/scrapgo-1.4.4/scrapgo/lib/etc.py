import math
from random import random


def gen_random_value(low:int, high:int, rounds=2):
    width = high - low
    v = low+random()*width
    return round(v, rounds)


def format_bytes_size(length, ndigits=None):
    k = 1024
    m = k**2
    g = k**3

    if length > k:
        unit = 'K'
        v = length / k
    elif length > m:
        unit = 'M'
        v = length / m
    elif length > g:
        unit = 'G'
        v = length / g
    else:
        unit = 'bytes'
        v = length
    return f'{round(v, ndigits)}{unit}'


def array2matrix(array:list, n:int, orphan=True):
    length = len(array)
    s, e = 0, n
    result = []
    while e < length:
        slc = array[s:e]
        s = e
        e = e + n
        result.append(slc)

    rest = array[s:e]
    is_orphan = rest and len(rest) < n

    if not is_orphan:
        result.append(rest)
    
    if is_orphan:
        if orphan:
            result.append(rest)
    return result


def get_next_rotate(iterable, current):
    rotater = list(iterable) * 2
    for i, value in enumerate(rotater):
        if current == value:
            return rotater[i+1]
    raise ValueError(f'Cannot find {current} in {iterable}')


def get_rotate(iterable):
    if iterable:
        first, *rest = iterable
        return [*rest, first]
    raise ValueError(f'{iterable}must have at least one element')


def npaginator(page_size, total, start=1, step=1):
    last = math.ceil(total / page_size)
    if start == 0:
        yield from range(start, last, step)
    else:
        yield from range(start, last + 1, step)
