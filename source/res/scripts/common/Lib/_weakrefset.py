# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/common/Lib/_weakrefset.py
# Compiled at: 1992-08-11 10:19:06
from _weakref import ref
__all__ = ['WeakSet']

class _IterationGuard(object):

    def __init__(self, weakcontainer):
        self.weakcontainer = ref(weakcontainer)

    def __enter__(self):
        w = self.weakcontainer()
        if w is not None:
            w._iterating.add(self)
        return self

    def __exit__(self, e, t, b):
        w = self.weakcontainer()
        if w is not None:
            s = w._iterating
            s.remove(self)
            if not s:
                w._commit_removals()
        return


class WeakSet(object):

    def __init__(self, data=None):
        self.data = set()

        def _remove(item, selfref=ref(self)):
            self = selfref()
            if self is not None:
                if self._iterating:
                    self._pending_removals.append(item)
                else:
                    self.data.discard(item)
            return

        self._remove = _remove
        self._pending_removals = []
        self._iterating = set()
        if data is not None:
            self.update(data)
        return

    def _commit_removals(self):
        l = self._pending_removals
        discard = self.data.discard
        while l:
            discard(l.pop())

    def __iter__(self):
        with _IterationGuard(self):
            for itemref in self.data:
                item = itemref()
                if item is not None:
                    yield item

        return

    def __len__(self):
        return len(self.data) - len(self._pending_removals)

    def __contains__(self, item):
        try:
            wr = ref(item)
        except TypeError:
            return False

        return wr in self.data

    def __reduce__(self):
        return (self.__class__, (list(self),), getattr(self, '__dict__', None))

    __hash__ = None

    def add(self, item):
        if self._pending_removals:
            self._commit_removals()
        self.data.add(ref(item, self._remove))

    def clear(self):
        if self._pending_removals:
            self._commit_removals()
        self.data.clear()

    def copy(self):
        return self.__class__(self)

    def pop(self):
        if self._pending_removals:
            self._commit_removals()
        while True:
            try:
                itemref = self.data.pop()
            except KeyError:
                raise KeyError('pop from empty WeakSet')

            item = itemref()
            if item is not None:
                return item

        return

    def remove(self, item):
        if self._pending_removals:
            self._commit_removals()
        self.data.remove(ref(item))

    def discard(self, item):
        if self._pending_removals:
            self._commit_removals()
        self.data.discard(ref(item))

    def update(self, other):
        if self._pending_removals:
            self._commit_removals()
        for element in other:
            self.add(element)

    def __ior__(self, other):
        self.update(other)
        return self

    def difference(self, other):
        newset = self.copy()
        newset.difference_update(other)
        return newset

    __sub__ = difference

    def difference_update(self, other):
        self.__isub__(other)

    def __isub__(self, other):
        if self._pending_removals:
            self._commit_removals()
        if self is other:
            self.data.clear()
        else:
            self.data.difference_update((ref(item) for item in other))
        return self

    def intersection(self, other):
        return self.__class__((item for item in other if item in self))

    __and__ = intersection

    def intersection_update(self, other):
        self.__iand__(other)

    def __iand__(self, other):
        if self._pending_removals:
            self._commit_removals()
        self.data.intersection_update((ref(item) for item in other))
        return self

    def issubset(self, other):
        return self.data.issubset((ref(item) for item in other))

    __le__ = issubset

    def __lt__(self, other):
        return self.data < set((ref(item) for item in other))

    def issuperset(self, other):
        return self.data.issuperset((ref(item) for item in other))

    __ge__ = issuperset

    def __gt__(self, other):
        return self.data > set((ref(item) for item in other))

    def __eq__(self, other):
        return NotImplemented if not isinstance(other, self.__class__) else self.data == set((ref(item) for item in other))

    def __ne__(self, other):
        opposite = self.__eq__(other)
        return NotImplemented if opposite is NotImplemented else not opposite

    def symmetric_difference(self, other):
        newset = self.copy()
        newset.symmetric_difference_update(other)
        return newset

    __xor__ = symmetric_difference

    def symmetric_difference_update(self, other):
        self.__ixor__(other)

    def __ixor__(self, other):
        if self._pending_removals:
            self._commit_removals()
        if self is other:
            self.data.clear()
        else:
            self.data.symmetric_difference_update((ref(item, self._remove) for item in other))
        return self

    def union(self, other):
        return self.__class__((e for s in (self, other) for e in s))

    __or__ = union

    def isdisjoint(self, other):
        return len(self.intersection(other)) == 0
