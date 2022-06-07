
""" Eine dynamische Ecke ist eine bewegliche Ecke in einem Statik-Objekt."""

import numpy as np
from matplotlib import path
from .ecke import ecke


class dynamische_ecke(ecke):
    
    
    def __init__(self, sphäre, position, ans_kraft = "DEFAULT"):
        """ Im Statik-Objekt werden alle Kräfte der dynamischen Ecke gespeichert. Es gibt deinen Speicherplatz hierfür in der dynamischen_ecke selbst.
        """
        
        super().__init__(sphäre)    # Gebe dem Objekt eine Nummer
                                    # Inkludiere die Ecke in der Sphäre
                                    # Erstelle self.kanten
        if ans_kraft == "DEFAULT":
            ans_kraft = np.array([0 for i in position[0:-1]] + [-1]) * self.masse
        
        self.sphäre.ecken_ans[self.spb] = ans_kraft
        self.sphäre.ecken_res[self.spb] = [0] * self.sphäre.dim
        self.sphäre.ecken_pos[self.spb] = position
        
        self.sphäre.ecken_geschwindigkeit[self.spb] = np.zeros(len(position))  # Hier nicht wirklich nötig, darf jedoch keinen Fehler werden.
        self.sphäre.ecken_beschleunigung[self.spb] = np.zeros(len(position))  # Das selbe gilt hierfür
        self.sphäre.ecken_masse[self.nummer] = 1
    
    def __del__(self):
        super().__del__()
    
    #def bewege(self, dynamik, zeitänderung):
        """
        Sobald Bewegungen von Ecken implementiert werden bedarf diese Funktion einer Überarbeitung.
        
        # Trenne noch die Geschwindigkeit für große Bewegungen von Geschwindigkeiten kleiner Bewegungen.
        
        self.beschleunigung = self.res_kraft / self.masse
        self.geschwindigkeit += self.beschleunigung * zeitänderung
        self.position += self.geschwindigkeit * zeitänderung
        
        dynamik.kanten_real |= {k.berechne_reale_kraft for k in self.kanten}
        dynamik.ecken_update.add(self.update)
        if (sum(self.mikro_geschwindigkeit**2) >= (0.01 / self.masse * zeitänderung)**2).any():
            dynamik.ecken_bewege.add(self.bewege)
        """
    #    pass
    
    #def update(self, *args):
        """ Update für Dynamik bzw. Events """
    #    pass
    
    @property
    def ans_kraft(self):
        return self.sphäre.ecken_ans[self.spb()]
    
    #def setze_ans_kraft(self, ans_kraft):
    #    self.sphäre.ecken_ans[self.spb] = ans_kraft
        
    @property
    def res_kraft(self):
        return self.sphäre.ecken_res[self.spb()]
    
    #def setze_res_kraft(self, res_kraft):
    #    self.sphäre.ecken_res[self.spb] = res_kraft
    
    @property
    def reale_kraft(self):
        return sum([k.reale_kraft * self.richtung_von(k.gib_nachbar(self)) for k in self.kanten]) + self.ans_kraft
    
    @property
    def position(self):
        return self.sphäre.ecken_pos[self.spb]
    
    @property
    def geschwindigkeit(self):
        return self.sphäre.ecken_geschwindigkeit[self.spb]
    
    @property
    def beschleunigung(self):
        self.sphäre.ecken_beschleunigung[self.spb]
    
    @property
    def masse(self):
        self.sphäre.ecken_masse[self.nummer]
    

    def __str__(self):
        return (super().__str__()
                + "\n Masse : " + str(self.masse)
                + "\n Ansetzende Kraft: " + str(self.ans_kraft)
                + "\n Resultierende Kraft: " + str(self.res_kraft)
                + "\n Reale Kraft: " + str(self.reale_kraft))
