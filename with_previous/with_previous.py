def with_previous(iterable,fillValue=None):
    previous=fillValue
    for item in iterable:
        yield item,previous
        previous = item