
""" Diese Klasse implementiert alle physikalischen Gesetzmäßigkeiten mithilfe der drei Module:
        statik
        dynamik
        korrektur
"""
import numpy as np

from .statik import statik
from .dynamik import dynamik
from .korrektur import korrektur

class physik:
    
    def __init__(self, sphäre, num_ecken, num_kanten, dim = 2):
        self.statik = statik(sphäre, num_kanten)
        self.dynamik = dynamik(sphäre)
        # self.korrektur = korrektur(...)
        
        self.sphäre = sphäre
    
    def berechne(self, zeitänderung):
    
        # Berechnung der durch die Erdbeschleunigung und Masse einwirkenden Kräfte auf die Eckpunkte
        g = np.matrix([0 for i in range(self.sphäre.dim - 1)] + [-10]).T # Erdbeschleunigung
        self.sphäre.ecken_ans = np.array((g * self.sphäre.ecken_masse).T).reshape((1, -1)).flatten()
        
        self.statik.berechne()
        ecken = self.dynamik.berechne(zeitänderung)
        self.statik.revidiere(ecken)
        
        # korrektur