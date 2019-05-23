"""
Here is a simple example of a class that implements the preceding methods to create a
sequence where items are always stored in sorted order (it’s not a particularly efficient
implementation, but it illustrates the general idea):
"""

import collections
import bisect


class SortedItems(collections.Sequence):
    def __init__(self, initial=None):
        self._items = sorted(initial) if initial is None else []

    # Required sequence methods
    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)

    # Method for adding an item in the right location
    def add(self, item):
        bisect.insort(self._items, item)