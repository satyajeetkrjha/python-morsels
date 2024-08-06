from functools import wraps
import inspect


def get_argument_string(*args,**kwargs):
    if args:
        argument_string = ", ".join(repr(a) for a in args)
    else:
        argument_string= ""

    if kwargs:
        if argument_string:
            argument_string+=", "
        argument_string+= ", ".join(f"{name}={value!r}" for name,value in kwargs.items())
    return argument_string        





def debug_calls(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        argument_string = get_argument_string(*args,**kwargs)
        info = inspect.stack()[1] # most important part
        print(
            f"{func.__name__}({argument_string})"
            f" called by {info.function}"
            f" in file {info.filename!r}"
            f" on line {info.lineno}"
        )
        return func(*args,**kwargs)
    return wrapper


