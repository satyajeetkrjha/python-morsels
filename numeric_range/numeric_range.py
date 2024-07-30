def numeric_range(iterable):
    iterator = iter(iterable)
    try:
        minimum =maximum = next(iterator)
    except StopIteration:
        minimum =maximum = 0

    for item in iterable:
        if item > maximum:
            maximum = item

        if item < minimum:
            minimum = item
    return maximum - minimum                    
