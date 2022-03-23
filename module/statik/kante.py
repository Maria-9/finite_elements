
""" Eine Kante stellt die Kante im Graphen einer Finiten-Elemente Analyse dar."""

from matplotlib import path
from .nummeriert import nummeriert
from messagebox import msg
import numpy as np
import math

class kante(nummeriert):

    def __init__(self, ecke1, ecke2, statik, kraft_limit=20, elastizitätsmodul = 0.9):
        
        super().__init__()
        self.kraft_limit = kraft_limit
        self.elastizitätsmodul = elastizitätsmodul

        self.ecke1 = ecke1
        self.ecke2 = ecke2

        self.natürliche_länge = np.linalg.norm(ecke1.position - ecke2.position)

        self.ecke1.neue_kante(self)
        self.ecke2.neue_kante(self)
        
        self.statik = statik
        self.statik.inkludiere(self)

    
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
    
    @property
    def res_kraft(self):
        return self.statik.kanten_res[self.nummer]
    
    @res_kraft.setter
    def setze_res_kraft(self, res_kraft):
        self.statik.kanten_res[self.nummer] = res_kraft
    
    def gib_reale_kraft(self):
        aktuelle_länge = np.linalg.norm(self.ecke1.position - self.ecke2.position)
        
        # Unter der Annahme eines linearen Verhältnisses von gestauchter Strecke zur aufgewendeten Kraft.
        #return self.elastizitätsmodul * (1 - aktuelle_länge / self.natürliche_länge)
        
        # Unter der Annahme eines antiproportionalen Verhältnisses von gestauchter Strecke zur aufgewendeten Kraft.
        #return self.elastizitätsmodul * (self.natürliche_länge / aktuelle_länge - 1)
        
        # Im wesentlichen ist eine Differentialgleichung gegeben:
        #   l'(f) = (f * l(f)^2) / (V * E)  , wobei
        #   l(f) Die Länge des Stabes bei einwirkender Kraft f ist
        #   V das Volumen des Stabes, und
        #   E das Elastizitätsmodul
        #
        # Wofram Alpha schlägt als Lösung f = sqrt( 2*E*V*(1 - L/l) ) vor, dies entspricht in etwa der Wurzel des obigen antiproportionalen Verhältnisses.
        # Nehmen wir an, dass das Volumen eines Stabes proportional zu seiner Länge zunimmt ergibt sich
        
        antiprop = self.elastizitätsmodul * self.natürliche_länge * (self.natürliche_länge / aktuelle_länge - 1)
        return math.sqrt(antiprop) if antiprop >= 0 else -math.sqrt(-antiprop)
        
    def __del__(self):
        msg.info("Shall I get deleted?")
        super().__del__()
    
    def delete(self, *objects):
        msg.info("Entferne eine Kante")
        self.statik.exkludiere(self)
        self.ecke1.kanten.remove(self)
        self.ecke2.kanten.remove(self)
          
    def __str__(self):
        return (super().__str__()
                + "\n Ecken: [" + str(self.ecke1.nummer) + ", " + str(self.ecke2.nummer) + "]")
