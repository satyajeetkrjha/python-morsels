from keyword import iskeyword
from dataclasses import make_dataclass

#https://chatgpt.com/share/967af5aa-9e15-4e3a-9eaa-8c1e7621f806
def make_class(name,arguments,*,restrict_attrs=False):
    if isinstance(arguments,str):
        arguments = arguments.split(" ")

    invalid = [arg for arg in arguments if iskeyword(arg) or not arg.isidentifier()]
    if invalid:
        raise ValueError(f"Invalid arguments: {', '.join(invalid)}")
    return make_dataclass(name,arguments,slots= restrict_attrs)    
