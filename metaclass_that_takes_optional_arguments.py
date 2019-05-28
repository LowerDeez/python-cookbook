"""
Problem
You want to define a metaclass that allows class definitions to supply optional argu‐
ments, possibly to control or configure aspects of processing during type creation.

Solution
To support such keyword arguments in a metaclass, make sure you define them on the
__prepare__(), __new__(), and __init__() methods using keyword-only arguments,
like this:
"""


class MyMeta(type):
    # Optional
    @classmethod
    def __prepare__(cls, name, bases, *, debug=False, synchronize=False):
        # Custom processing
        ...
        return super().__prepare__(name, bases)
    
    # Required
    def __new__(cls, name, bases, ns, *, debug=False, synchronize=False):
        # Custom processing
        ...
        return super().__new__(cls, name, bases, ns)
    
    # Required
    def __init__(self, name, bases, ns, *, debug=False, synchronize=False):
        # Custom processing
        ...
        super().__init__(name, bases, ns)


class Spam(metaclass=MyMeta, debug=True, synchronize=True):
    ...
