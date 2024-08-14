def coalesce(value, default, *, sentinel=None):
    if isinstance(sentinel,tuple):
        sentinels = sentinel
    else:
        sentinels = (sentinel,)
    for item in sentinels:
        if item == value:
            return default
    return value    
