"""
To define a decorator as an instance, you need to make sure it implements the
__call__() and __get__() methods. For example, this code defines a class that puts a
simple profiling layer around another function:
"""


import types
from functools import wraps


class Profiled:
    def __init__(self, func):
        wraps(func)(self)
        self.ncalls = 0

    def __call__(self, *args, **kwargs):
        self.ncalls += 1
        return self.__wrapped__(*args, **kwargs)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)


# To use this class, you use it like a normal decorator, either inside or outside of a class:

@Profiled
def add(x, y):
    return x + y

class Spam:
    @Profiled
    def bar(self, x):
        print(self, x)


"""
In this recipe, the __get__() method is there to make sure bound method objects get
created properly. type.MethodType() creates a bound method manually for use here.
Bound methods only get created if an instance is being used. If the method is accessed
on a class, the instance argument to __get__() is set to None and the Profiled instance
itself is just returned. This makes it possible for someone to extract its ncalls attribute,
as shown.
If you want to avoid some of this of this mess, you might consider an alternative for‐
mulation of the decorator using closures and nonlocal variables, as described in
Recipe 9.5. For example:
"""

import types
from functools import wraps


def profiled(func):
    ncalls = 0
    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal ncalls
        ncalls += 1
        return func(*args, **kwargs)
    wrapper.ncalls = lambda: ncalls
    return wrapper

# Example
@profiled
def add(x, y):
    return x + y

"""
This example almost works in exactly the same way except that access to ncalls is now
provided through a function attached as a function attribute. For example:
>>> add(2, 3)
5
>>> add(4, 5)
9
>>> add.ncalls()
2
>>>
"""