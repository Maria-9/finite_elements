
""" Dynamik merklicher Bewegungen. Diese Klasse ist nicht für minimale Zustandsänderungen gedacht. """

from .kante import kante
from .dynamische_ecke import dynamische_ecke
from .statische_ecke import statische_ecke
import numpy as np

class dynamik:
    
    def __init__(self, sphäre):
        self.sphäre = sphäre
    
    def berechne(self, zeitänderung):
        # Es kann sich lohnen minimale Beschleunigungen, sowie minimale Geschwindigkeiten und minimale Positionsänderugen zu vernachlässigen.
        # Unter Umständen zieht dies jedoch Probleme mit sich.
        
        self.sphäre.ecken_beschleunigung = (self.sphäre.ecken_res
                                            / np.array([self.sphäre.ecken_masse] * self.sphäre.dim).T.reshape((1, -1)).flatten())
        #print("F:")
        #print((self.sphäre.ecken_res - self.sphäre.ecken_ans))
        self.sphäre.ecken_geschwindigkeit += self.sphäre.ecken_beschleunigung * zeitänderung
        self.sphäre.ecken_pos += self.sphäre.ecken_geschwindigkeit * zeitänderung