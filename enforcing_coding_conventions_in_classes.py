"""
Problem
Your program consists of a large class hierarchy and you would like to enforce certain
kinds of coding conventions (or perform diagnostics) to help maintain programmer
sanity.

Solution
If you want to monitor the definition of classes, you can often do it by defining a
metaclass. A basic metaclass is usually defined by inheriting from type and redefining
its __new__() method or __init__() method.
A key feature of a metaclass is that it allows you to examine the contents of a class at the
time of definition.
Inside the redefined __init__() method, you are free to inspect the
class dictionary, base classes, and more. Moreover, once a metaclass has been specified
for a class, it gets inherited by all of the subclasses. Thus, a sneaky framework builder
can specify a metaclass for one of the top-level classes in a large hierarchy and capture
the definition of all classes under it.
As a concrete albeit whimsical example, here is a metaclass that rejects any class defi‐
nition containing methods with mixed-case names (perhaps as a means for annoying
Java programmers):
"""

class NoMixedCaseMeta(type):
    def __new__(cls, clsname, bases, clsdict):
        for name in clsdict:
            if name.lower() != name:
                raise TypeError('Bad attribute name: ' + name)
        return super().__new__(cls, clsname, bases, clsdict)


class Root(metaclass=NoMixedCaseMeta):
    pass


class A(Root):
    def foo_bar(self): # Ok
        pass


class B(Root):
    def fooBar(self): # TypeError
        pass


"""
As a more advanced and useful example, here is a metaclass that checks the definition
of redefined methods to make sure they have the same calling signature as the original
method in the superclass.
"""


from inspect import signature
import logging


class MatchSignaturesMeta(type):
    def __init__(self, clsname, bases, clsdict):
        super().__init__(clsname, bases, clsdict)
        sup = super(self, self)
        for name, value in clsdict.items():
            if name.startswith('_') or not callable(value):
                continue
            # Get the previous definition (if any) and compare the signatures
            prev_dfn = getattr(sup,name,None)
            if prev_dfn:
                prev_sig = signature(prev_dfn)
                val_sig = signature(value)
                if prev_sig != val_sig:
                    logging.warning('Signature mismatch in %s. %s != %s',
                        value.__qualname__, prev_sig, val_sig)


# Example
class Root(metaclass=MatchSignaturesMeta):
    pass


class A(Root):
    def foo(self, x, y):
        pass

    def spam(self, x, *, z):
        pass


# Class with redefined methods, but slightly different signatures
class B(A):
    def foo(self, a, b):
        pass

    def spam(self,x,z):
        pass
