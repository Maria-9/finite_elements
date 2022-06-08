
""" Eine Kante stellt die Kante im Graphen einer Finiten-Elemente Analyse dar."""

from matplotlib import path
from .nummeriert import nummeriert
from messagebox import msg
import numpy as np
import math

class kante(nummeriert):

    def __init__(self, sphäre, ecke1, ecke2, länge = "DEFAULT", kraft_limit=15, elastizitätsmodul = 10000):
        
        super().__init__()
        
        self.ecke1 = ecke1      # Diese Informationen werden vorerst weiter in der Kante gespeichert, ev. kann man sie in die Sphäre auslagen.
        self.ecke2 = ecke2
        self.ecke1.neue_kante(self)
        self.ecke2.neue_kante(self)
        
        self.sphäre = sphäre
        self.sphäre.inkludiere(self)
        
        if länge == "DEFAULT":
            länge = np.linalg.norm(ecke1.position - ecke2.position)
        
        self.sphäre.kanten_natürliche_länge[self.nummer] = länge
        self.sphäre.kanten_kraft_limit[2*self.nummer : 2*(self.nummer + 1)] = [-kraft_limit, kraft_limit] # Die Grenzen für einwirkende Kräfte
        self.sphäre.kanten_elastizitätsmodul[self.nummer] = elastizitätsmodul
        self.sphäre.kanten_real[self.nummer] = 0  
                                # diese Kraft wird für die Berechnung der Dynamik benötigt. Sie errechnet sich aus der durch die Stauchung oder 
                                # Dehnung der Kante entstehenden Kraft auf die Eckpunkte der Kante.
    
    def gib_nachbar(self, ecke):
        if ecke is self.ecke1:
            return self.ecke2
        if ecke is self.ecke2:
            return self.ecke1
        msg.error("Die Ecke ist kein Endpunkt der Kante")
        return None
    
    def auflösen(self):
        self.ecke1.entferne_kante(self)
        self.ecke2.entferne_kante(self)
        self.sphäre.exludiere(self)
    
    @property
    def res_kraft(self):
        return self.sphäre.kanten_res[self.nummer]

    @property
    def reale_kraft(self):
        return self.sphäre.kanten_real[self.nummer]
    
    @property
    def kraft_limit(self):
        return self.sphäre.kanten_kraft_limit[2*self.nummer : 2*(self.nummer + 1)]
    
    def delete(self, *objects):
        msg.info("kante.delete wurde aufgerufen. Die Kantennummer ist " + str(self.nummer))
        self.sphäre.exkludiere(self)
        self.ecke1.kanten.remove(self)
        self.ecke2.kanten.remove(self)
          
    def __str__(self):
        return (super().__str__()
                + "\n Ecken: [" + str(self.ecke1.nummer) + ", " + str(self.ecke2.nummer) + "]")
