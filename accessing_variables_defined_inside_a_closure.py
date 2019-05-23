"""
Problem
You would like to extend a closure with functions that allow the inner variables to be
accessed and modified.
Solution
Normally, the inner variables of a closure are completely hidden to the outside world.
However, you can provide access by writing accessor functions and attaching them to
the closure as function attributes. For example:
"""
def sample():
    n = 0

    # Closure function
    def func():
        print('n=', n)

    # Accessor methods for n
    def get_n():
        return n

    def set_n(value):
        nonlocal n
        n = value
    
    # Attach as function attributes
    func.get_n = get_n
    func.set_n = set_n
    return func

"""
Here is an example of using this code:
>>> f = sample()
>>> f()
n= 0
>>> f.set_n(10)
>>> f()
n= 10
>>> f.get_n()
10
>>>
"""