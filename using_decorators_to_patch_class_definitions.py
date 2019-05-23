"""
This might be a perfect use for a class decorator. For example, here is a class decorator
that rewrites the __getattribute__ special method to perform logging.
"""

def log_getattribute(cls):
    # Get the original implementation
    orig_getattribute = cls.__getattribute__
    
    # Make a new definition
    def new_getattribute(self, name):
        print('getting:', name)
        return orig_getattribute(self, name)

    # Attach to the class and return
    cls.__getattribute__ = new_getattribute
    return cls

# Example use
@log_getattribute
class A:
    def __init__(self,x):
        self.x = x

    def spam(self):
        pass

"""
Here is what happens if you try to use the class in the solution:
>>> a = A(42)
>>> a.x
getting: x
42
>>> a.spam()
getting: spam
>>>
"""