from collections.abc import Iterable
#This solution handles iterables of type list and tuples

def deep_flatten(iterables):
    flattened=[]
    for item in iterables:
        if isinstance(item,(list,tuple)):
            flattened.extend(deep_flatten(item))
        else:
            flattened.append(item)
    return flattened            
            


def deep_flatten(iterables):
    flattened =[]
    for item in iterables:
        if hasattr(item,'__iter__'): # or if isinstance(item,Iterable)
            flattened.extend(deep_flatten(item))
        else:
            flattened.append(item)
    return flattened                                   
            
        

def deep_flatten(iterable):
    for item in iterable:
        if isinstance(item,Iterable):
            for x in deep_flatten(item):
                yield x    
        else:
            yield item
                    
    