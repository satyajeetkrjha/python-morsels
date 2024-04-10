# def chunked(sequence,n):
#     return [sequence[i:n+1] for i in range(0,len(sequence),n)]

from itertools import islice
def chunked(iterable,n):
    iterator = iter(iterable)
    chunks =[]
    
    while True:
        items = tuple(islice(iterator,n))
        if not items:
            break
        chunks.append(items)
    return chunks    
         
