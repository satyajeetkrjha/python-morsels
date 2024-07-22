def only_once(func):
    called = False
    @wraps(func)
    def wrapper(*args,**kwargs):
        nonlocal called
        if called:
            raise ValueError("You can't call this function twice!")
        called = True
        return func(*args,**kwargs)
    return wrapper        

