
from dataclasses import astuple
class Point: 
    
    def __init__(self,x,y,z) -> None:
        self.x,self.y,self.z = x,y,z
    
    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z
    
    def __repr__(self) -> str:
        return f"Point(x={self.x} ,y={self.y} ,z={self.z})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other,Point):
            raise NotImplemented
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __add__(self,other):
        if not isinstance(other,Point):
            raise NotImplemented
        return Point(self.x + other.x,self.y + other.y,self.z + other.z)
    
    def __sub__(self,other):
        if not isinstance(other,Point):
            raise NotImplemented
        return Point(self.x - other.x,self.y - other.y,self.z - other.z)
    
    def __mul__(self,scalar):
        if not isinstance(scalar,(int,float)):
            raise NotImplemented
        return Point(scalar*self.x,scalar*self.y,scalar*self.z)
    __rmul__=__mul__



p1 = Point(1,2,3)
print(p1)
p2 = Point(1,2,3)
print(p2)   
print(p1==p2)
print(p1+p2)
print(p1-p2)
p3 = p2*2
print(p3)
p4= 2*p2
print(p4)
x,y,z= p1
print(x)
print(y)
print(z)            