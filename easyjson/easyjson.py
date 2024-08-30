from json import loads

class JSONObject:

    def __init__(self, obj):
        self._data = obj  

    def __getitem__(self, key):
        if isinstance(key, tuple):
            return JSONObject({
                name: self[name]
                for name in key
            })
        return self._data[key] 
       
    def __getattr__(self, name):
        return self[name]  

    def __repr__(self):
        return repr(self._data)
    
    def __eq__(self, other):
        return self._data.__eq__(other)

    def keys(self):
        return self._data.keys()


def parse(json_string):
    return loads(json_string, object_hook=JSONObject)
