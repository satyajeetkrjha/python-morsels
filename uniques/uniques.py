
# def uniques_only(iterable):
#     items =[]
#     unique =set()
#     for item in iterable:
#         if item not in unique:
#             items.append(item)
#             unique.add(item)
#     return items 
    
    

# def uniques_only(iterable):
#     items =[]
#     for item in iterable:
#         if item not in items:
#             yield item
#             items.append(item) 
        

from collections.abc import Hashable
def uniques_only(iterable):
    hashable_item = set()
    unhashable_item = list()
    for item in iterable:
        if isinstance(item,Hashable):
            if item not in hashable_item:
                yield item
                hashable_item.add(item)
        else:
            if item not in unhashable_item:
                yield item
                unhashable_item.append(item)        
                
        