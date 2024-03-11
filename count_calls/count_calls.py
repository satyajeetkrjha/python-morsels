
# def count_calls():
#     def wrapper():
#         wrapper.calls+=1
#     wrapper.calls =0
#     return wrapper         

from math import sqrt
from functools import wraps

def count_calls(func = lambda:None):
    @wraps(func)
    def wrapper(*args,**kwargs):
        wrapper.calls+=1
        return func(*args,**kwargs)
    wrapper.calls =0
    wrapper.__annotations__ = func.__annotations__
    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    wrapper.__qualname__ = func.__qualname__
    return wrapper 
            


@count_calls
def quadratic(a, b, c):
    x1 = -b / (2*a)
    x2 = sqrt(b**2 - 4*a*c) / (2*a)
    return (x1 + x2), (x1 - x2)


print(quadratic(2, 8, 6))
print(quadratic.calls) 
print(help(quadratic))               