
""" Dynamik merklicher Bewegungen. Diese Klasse ist nicht für minimale Zustandsänderungen gedacht. """

from .kante import kante
from .dynamische_ecke import dynamische_ecke
from .statische_ecke import statische_ecke
import numpy as np

class dynamik:
    
    def __init__(self, sphäre):
        self.sphäre = sphäre
    
    def berechne(self, zeitänderung):
        """ Returns: Nummern der Ecken, die sich veränderten.""" 
        
        # Es kann sich lohnen minimale Beschleunigungen, sowie minimale Geschwindigkeiten und minimale Positionsänderugen zu vernachlässigen.
        # Unter Umständen zieht dies jedoch Probleme mit sich.
        
        self.sphäre.ecken_beschleunigung = (self.sphäre.ecken_res
                                            / np.array([self.sphäre.ecken_masse] * self.sphäre.dim).T.reshape((1, -1)).flatten())
        #print("A:")
        #print(self.sphäre.ecken_beschleunigung)
        self.sphäre.ecken_geschwindigkeit += self.sphäre.ecken_beschleunigung * zeitänderung
        
        eps = 0.0001
        v = (self.sphäre.ecken_geschwindigkeit > eps) + (self.sphäre.ecken_geschwindigkeit < -eps)
        self.sphäre.ecken_geschwindigkeit = self.sphäre.ecken_geschwindigkeit * v
        
        self.sphäre.ecken_pos += self.sphäre.ecken_geschwindigkeit * zeitänderung
        
        # Ermittle die Ecken deren Position sich veränderten
        
        nummern = np.array([i for i in range(len(self.sphäre.ecken_geschwindigkeit))])[v] // self.sphäre.dim
        # vermeide mehrfache Vorkommen
        nummern = np.array(list(set(nummern)))
        return [self.sphäre.dynamische_ecken[nummer] for nummer in nummern]