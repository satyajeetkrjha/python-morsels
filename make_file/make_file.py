
from tempfile import NamedTemporaryFile
import os
class make_file:
    def __init__(self,contents =None,directory=None,mode ='wt',**kwargs):
        self.file = NamedTemporaryFile(mode =mode,delete =False ,dir = directory,**kwargs)
        if contents:
            self.file.write(contents)
        self.file.close()
    
    def __enter__(self):
        return self.file.name
    
    def __exit__(self,*args):
        os.remove(self.file.name)        