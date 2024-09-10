from collections import UserDict

class CollisionDIct(UserDict):
    def __init__(self,*args,**kwargs):
        self.overridden =[]
        super().__init__(*args,**kwargs)


    def __setitem__(self, key ,value):
        if (key in self and (callable(value) or hasattr(value, '__get__')) and not isinstance(value, property)):
            self.overridden.append(key)
        super().__setitem__(key, value)

class NoMethodCollisionsType(type):

    def __new__(cls,name, bases,namespace):
        if namespace.overridden:
            attr = namespace.overridden[0]
            raise TypeError(f"{attr} specified multiple times on {name}.")
        return super().__new__(cls, name, bases, dict(namespace)) 

    @classmethod
    def __prepare__(metaclass ,name, bases):
        return CollisionDIct()


class NoMethodCollisions(metaclass=NoMethodCollisionsType):
    """class """





