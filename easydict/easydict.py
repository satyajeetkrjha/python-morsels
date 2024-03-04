class EasyDict:
    def __init__(self,mapping={},**kwargs):
        if mapping is not None:
            self.__dict__.update(mapping)
            self.__dict__.update(kwargs)
            
    def __getitem__(self,key):
        # return self.__dict__[key] 
        return getattr(self,key)
    
    def __setitem__(self,key,value):
        # self.__dict__[key] =value 
        setattr(self,key,value)
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value,EasyDict):
            raise NotImplemented
        return self.__dict__ == __value
             
    def get(self,key,default =None):
        return getattr(self,key,default)
                

easydict = EasyDict({'a': 2, 'b': 3})
       
       