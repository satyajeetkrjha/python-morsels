
from collections.abc import MutableSet
class OrderedSet(MutableSet):
    def __init__(self,iterable=()) -> None:
        # we created a dictionary here where key is the iterable item and all keys value None
        self.items = dict.fromkeys(iterable,None) 
    
    def __contains__(self, x) -> bool:
        return x in self.items    
    
    def __len__(self):
        return len(self.items)
    
    def __iter__(self):
        return iter(self.items.keys())
    
    def __eq__(self, other) -> bool:
        if isinstance(other ,type(self)):
            return (len(self) == len(other) and all (x == y for x,y in zip(self,other)))
        return super().__eq__(other)
    
    def add(self,item):
        self.items[item] =None
    
    def discard(self, item) -> None:
        return self.items.pop(item,None)  
    
    def __repr__(self):
        return f"{type(self).__name__}({list(self.items)})" 
        
        
    