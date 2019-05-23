def frange(start, stop, increment):
    x = start
    while x < stop:
        yield x
        x += increment