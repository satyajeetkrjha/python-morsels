from collections import defaultdict
def group_by(iterable, key_func=None):
    groups = defaultdict(list)#list factory
    if key_func is None:
        key_func= lambda x:x
    for item in iterable:
        groups[key_func(item)].append(item)

    return groups