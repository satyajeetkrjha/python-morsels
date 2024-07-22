from collections import defaultdict
from collections.abc import MutableMapping

class _DeletedValue:
    """ Value was deleted"""
    def __repr__(self):
        return "DELETED"


DELETED = _DeletedValue()

class HistoryDict(MutableMapping):
    def __init__(self, data =()):
        self._history = defaultdict(list)
        self.update(data)

    def __setitem__(self,key,value):
        self._history[key].append(value)

    def __getitem__(self,key):
        if key not in self._history:
            raise KeyError(key)
        value = self._history[key][-1]
        if value is DELETED:
            raise KeyError(key)
        return value

    def __delitem__(self,key):
        self._history[key].append(DELETED)

    def __len__(self):
        return len(self._history)

    def __iter__(self):
        for key,values in self._history.items():
            if values[-1] is not DELETED:
                yield key

    @property
    def _data(self):
        return {
            key: values[-1]
            for key, values in self._history.items()
            if values[-1] is not DELETED
        }

    def history(self, key):
        return self._history.get(key, [])

    def __repr__(self):
        return f"HistoryDict({self._data!r})"

    def all_history(self):
        return self._history    



