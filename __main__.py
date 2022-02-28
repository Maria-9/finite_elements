"""
from module.statik import *
from module.universen.universum1 import universum1
from messagebox import messagebox

msg = messagebox()
msg.state("Start")
#uni = universum1()
#uni.run()

from module.statik.matplot import plotable_object

class test:
    pass

x = plotable_object(test)
y = x()

print(y)
print(x)

a = plotable_object(test)
b = a()
c = a()

print(type(b) == type(y))
print(type(b) == type(c))
print(type(b))
print(type(y))
"""

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        
        print(getattr(cls, "_instances", False))
        cls._instances = {}
    
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
    
class SingletonClass(metaclass=Singleton):
    #_instances = {}
    pass
class SingletonClass2(metaclass=Singleton):
    #_instances = {}
    def __init__(self):
        print(getattr(self, "hallo", None)())
    def hallo(self):
        return("hallo")
class RegularClass():
    pass
x = SingletonClass()
y = SingletonClass()
a = SingletonClass()
z = SingletonClass2()
print(SingletonClass._instances)
print(SingletonClass2._instances)
print(Singleton._instances)
