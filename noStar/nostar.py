from math import tau
class NoStar:
    def __getitem__(self,index):
        raise ImportError("Don't use import *")



__all__ = NoStar()


