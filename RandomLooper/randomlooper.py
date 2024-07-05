
from itertools import chain
from random import shuffle

class RandomLooper:
    def __init__(self,*iterable):
        self.items = list(chain.from_iterable(iterable))
    
    def __iter__(self):
        shuffle(self.items)
        yield from self.items
    
    def __len__(self):
        return len(self.items)         