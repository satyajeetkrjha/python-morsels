def multimax(iterable,key=None):
    
    #identity function
    if key is None:
        def key(item):
            return item

    max_key =None
    maximums = []

    for item in iterable:
        k = key(item)
        if k == max_key:
            maximums.append(item)
        elif not maximums or k > max_key:
            maximums=[item]
            max_key = k   
    return maximums         


