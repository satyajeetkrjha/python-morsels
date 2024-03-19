
from numbers import Number
from dataclasses import dataclass

@dataclass(frozen=True)
class Vector:
    
    x:Number
    y:Number
    z:Number
    
    __slots__ = 'x','y','z'
    
    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z
    
    
    def __add__(self,other):
        if not isinstance(other,Vector):
            raise NotImplemented
        x1,y1,z1 = self 
        x2,y2,z2 = other
        return Vector(x1+x2,y1+y2,z1+z2)
    
    
    def __sub__(self,other):
        if not isinstance(other,Vector):
            raise NotImplemented
        x1,y1,z1 = self
        x2,y2,z2 = other
        
        return Vector(x1-x2,y1-y2,z1-z2)
    
    def __truediv__(self,scalar):
        if not isinstance(scalar,Number):
            raise NotImplemented
        
        x,y,z = self
        return Vector(x/scalar,y/scalar,z/scalar) 
        
    def __mul__(self,scalar):
        if not isinstance(scalar,Number):
            raise NotImplemented
        x,y,z = self
        return Vector(x*scalar,y*scalar,z*scalar)
    __rmul__=__mul__
    
        
           
    