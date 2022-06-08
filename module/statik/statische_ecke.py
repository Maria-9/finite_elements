
""" Eine Statische Ecke ist ein Fixpunkt im Graphen der Finiten Elemente-Methode. """

from .ecke import ecke 

class statische_ecke(ecke):
    
    def __init__(self, sphäre, position):
        super().__init__(sphäre)
        self.sphäre.stat_ecken_pos[self.spb] = position
    
    @property
    def position(self):
        return self.sphäre.stat_ecken_pos[self.spb]


