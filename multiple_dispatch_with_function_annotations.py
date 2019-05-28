"""
Problem
You’ve learned about function argument annotations and you have a thought that you
might be able to use them to implement multiple-dispatch (method overloading) based
on types. However, you’re not quite sure what’s involved (or if it’s even a good idea).
"""


import types


class multimethod:
    def __init__(self, func):
        self._methods = {}
        self.__name__ = func.__name__
        self._default = func

    def match(self, *types):
        def register(func):
            ndefaults = len(func.__defaults__) if func.__defaults__ else 0
            for n in range(ndefaults+1):
                self._methods[types[:len(types) - n]] = func
            return self
        return register

    def __call__(self, *args):
        types = tuple(type(arg) for arg in args[1:])
        meth = self._methods.get(types, None)
        if meth:
            return meth(*args)
        else:
            return self._default(*args)

    def __get__(self, instance, cls):
        if instance is not None:
            return types.MethodType(self, instance)
        else:
            return self

"""
To use the decorator version, you would write code like this:
"""


class Spam:
    @multimethod
    def bar(self, *args):
        # Default method called if no match
        raise TypeError('No matching method for bar')
    
    @bar.match(int, int)
    def bar(self, x, y):
        print('Bar 1:', x, y)
    
    @bar.match(str, int)
    def bar(self, s, n = 0):
        print('Bar 2:', s, n)