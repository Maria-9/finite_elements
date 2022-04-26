
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
            if obj == None:
                continue
            verts, codes, color = obj.verts_codes_color()
            obj_path = path.Path(verts, codes)
            patch = patches.PathPatch(obj_path, facecolor=color,
                                    edgecolor=color, alpha=0.5)
            self.ax.add_patch(patch)
    
    def draw(self, intervall=0.5):
        self.ax.set_xlim(0, self.shape[0])
        self.ax.set_ylim(0, self.shape[1])

        plt.draw()
        plt.pause(intervall)

    def show(self):
        plt.show()
    
    def cla(self):
        plt.cla()