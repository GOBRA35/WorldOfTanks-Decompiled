# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/common/Lib/functools.py
# Compiled at: 2057-07-16 23:38:49
"""functools.py - Tools for working with functions and callable objects
"""
from _functools import partial, reduce
WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__doc__')
WRAPPER_UPDATES = ('__dict__',)

def update_wrapper(wrapper, wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES):
    """Update a wrapper function to look like the wrapped function
    
       wrapper is the function to be updated
       wrapped is the original function
       assigned is a tuple naming the attributes assigned directly
       from the wrapped function to the wrapper function (defaults to
       functools.WRAPPER_ASSIGNMENTS)
       updated is a tuple naming the attributes of the wrapper that
       are updated with the corresponding attribute from the wrapped
       function (defaults to functools.WRAPPER_UPDATES)
    """
    for attr in assigned:
        setattr(wrapper, attr, getattr(wrapped, attr))

    for attr in updated:
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))

    return wrapper


def wraps(wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES):
    """Decorator factory to apply update_wrapper() to a wrapper function
    
       Returns a decorator that invokes update_wrapper() with the decorated
       function as the wrapper argument and the arguments to wraps() as the
       remaining arguments. Default arguments are as for update_wrapper().
       This is a convenience function to simplify applying partial() to
       update_wrapper().
    """
    return partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated)


def total_ordering(cls):
    """Class decorator that fills in missing ordering methods"""
    convert = {'__lt__': [('__gt__', lambda self, other: not (self < other or self == other)),
                ('__le__', lambda self, other: self < other or self == other),
                ('__ne__', lambda self, other: not self == other),
                ('__ge__', lambda self, other: not self < other)],
     '__le__': [('__ge__', lambda self, other: not self <= other or self == other),
                ('__lt__', lambda self, other: self <= other and not self == other),
                ('__ne__', lambda self, other: not self == other),
                ('__gt__', lambda self, other: not self <= other)],
     '__gt__': [('__lt__', lambda self, other: not (self > other or self == other)),
                ('__ge__', lambda self, other: self > other or self == other),
                ('__ne__', lambda self, other: not self == other),
                ('__le__', lambda self, other: not self > other)],
     '__ge__': [('__le__', lambda self, other: not self >= other or self == other),
                ('__gt__', lambda self, other: self >= other and not self == other),
                ('__ne__', lambda self, other: not self == other),
                ('__lt__', lambda self, other: not self >= other)]}
    defined_methods = set(dir(cls))
    roots = defined_methods & set(convert)
    if not roots:
        raise ValueError('must define at least one ordering operation: < > <= >=')
    root = max(roots)
    for opname, opfunc in convert[root]:
        if opname not in defined_methods:
            opfunc.__name__ = opname
            opfunc.__doc__ = getattr(int, opname).__doc__
            setattr(cls, opname, opfunc)

    return cls


def cmp_to_key(mycmp):
    """Convert a cmp= function into a key= function"""

    class K(object):
        __slots__ = ['obj']

        def __init__(self, obj, *args):
            self.obj = obj

        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0

        def __hash__(self):
            raise TypeError('hash not implemented')

    return K
