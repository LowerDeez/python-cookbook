class Date:
    __slots__ = ['year', 'month', 'day']
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day


"""
When you define __slots__, Python uses a much more compact internal representation
for instances. Instead of each instance consisting of a dictionary, instances are built
around a small fixed-sized array, much like a tuple or list. Attribute names listed in the
__slots__ specifier are internally mapped to specific indices within this array. A side
effect of using slots is that it is no longer possible to add new attributes to instances—
you are restricted to only those attribute names listed in the __slots__ specifier.
"""