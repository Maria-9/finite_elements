
""" Verwaltet das Zeichnen eines Plots der angegebenen Objekte. """

import matplotlib.patches as patches
import matplotlib.path as path
import matplotlib.pyplot as plt

class matplot:
    """
        Verwendung:
            mplt = matplot()
            mplt.add([obj1, obj2, obj3, ...])
            mplt.add([objA, objB, objC, ...])
            mplt.show()
    """
    def __init__(self, shape=(12,10)):
        self.fig, self.ax = plt.subplots()
        self.shape = shape

    def add(self, objects):
        for obj in objects:
            verts, codes, color = obj.verts_codes_color()
            obj_path = path.Path(verts, codes)
            patch = patches.PathPatch(obj_path, facecolor=color,
                                    edgecolor=color, alpha=0.5)
            self.ax.add_patch(patch)
    
    def show(self):
        self.ax.set_xlim(0, self.shape[0])
        self.ax.set_ylim(0, self.shape[1])
        
        plt.show()


# Erzeuge eine Metaklasse für Plotbare Funktionen

class ClassConverter(type):
    
    def __init__(self, *args, **kwargs):
        print(*args)
    
    def __call__(cls, *args, **kwargs):
        print(cls)
        print("-------")
        print(*args)
        #if cls not in cls.__converter_instances:
         #   cls.__init__ = lambda self, *args, **kwargs : None
          #  cls.__converter_instances[cls] = type.__call__(cls, *args, **kwargs)
        cls.dic = {}
        cls.__convert__ = ClassConverter.__convert__
        #cls.__no_conversion_defined = cls.__no_conversion_defined
        
        return cls.__convert__(args[0])
    
    @classmethod
    def __convert__(cls, convert):
        if convert in cls.__dict__:
            return self.__dict__[convert]
        print("cls: " + str(cls))
        print(cls.__class__.__dict__)
        cls.__dict__[convert] = getattr(cls, "__convert__" + convert.__name__, cls.__no_conversion_defined)(convert)
        return cls.__dict__[convert]
    
    @classmethod
    def __no_conversion_defined(cls, convert):
        print("__convert__" + convert.__name__)
        raise Exception(str(cls) + " has no conversion for class " + convert.__name__ + " defined.")



import abc

class plotable_object(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def verts_codes_color(cls, size):
        pass

class plotable(metaclass=ClassConverter):
    
    @classmethod
    def __convert__plotable_object(cls, other_cls):
        return int

if __name__ == "__main__":
    c = plotable(plotable_object)
    print(c)