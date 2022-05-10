
""" Eine dynamische Ecke ist eine bewegliche Ecke in einem Statik-Objekt."""

import numpy as np
from matplotlib import path
from .ecke import ecke


class dynamische_ecke(ecke):
    
    
    def __init__(self, position, statik, dynamik, ans_kraft = "DEFAULT"):
        """ Im Statik-Objekt werden alle Kräfte der dynamischen Ecke gespeichert. Es gibt deinen Speicherplatz hierfür in der dynamischen_ecke selbst.
        """
        
        super().__init__(position)
        self.masse = 1
        self.beschleunigung = np.zeros(len(position))
        self.geschwindigkeit = np.zeros(len(position))
        
        if ans_kraft == "DEFAULT":
            ans_kraft = np.array([0 for i in position[0:-1]] + [-1]) * self.masse
        
        dynamik.inkludiere(self)
        
        if statik.dim != self.dim:
            raise ValueError("Ein " + statik.dim + " dimensionales Statik-Objekt kommt nicht mit einer " + self.dim + " dimensionalen Ecke zurecht.")

        self.statik = statik
        self.statik.inkludiere(self)
        
        # Dies sind Attribute die auf den Speicher im Objekt self.statik zurückgreifen.
        self.setze_ans_kraft = ans_kraft
        self.setze_res_kraft = 0
    
    def __del__(self): 
        self.statik.exkludiere(self)
        super().__del__()
    
    
    def bewege(self, dynamik, zeitänderung):
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
        pass
    
    def update(self, *args):
        """ Update für Dynamik bzw. Events """
        pass

    def __stat_sp(self):
        # Gibt den Speicherbereich für die Kräfte im Statik Objekt zurück.
        return [self.nummer*self.dim + i for i in range(self.dim)]
    
    @property
    def ans_kraft(self):
        return self.statik.ecken_ans[self.__stat_sp()]
    
    @ans_kraft.setter
    def setze_ans_kraft(self, ans_kraft):
        self.statik.ecken_ans[self.__stat_sp()] = ans_kraft
        
    @property
    def res_kraft(self):
        return self.statik.ecken_res[self.__stat_sp()]
    
    @res_kraft.setter
    def setze_res_kraft(self, res_kraft):
        self.statik.ecken_res[self.__stat_sp()] = res_kraft
    
    @property
    def reale_kraft(self):
        return sum([k.reale_kraft * self.richtung_von(k.gib_nachbar(self)) for k in self.kanten]) + self.ans_kraft

    def __str__(self):
        return (super().__str__()
                + "\n Masse : " + str(self.masse)
                + "\n Ansetzende Kraft: " + str(self.ans_kraft)
                + "\n Resultierende Kraft: " + str(self.res_kraft)
                + "\n Reale Kraft: " + str(self.reale_kraft))
