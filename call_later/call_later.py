
def call_later(func,*args,**kwargs):
    def new_func():
        return func(*args,**kwargs)
    new_func.__doc__ = f"Calls {func} with {args} and {kwargs}"
    return new_func