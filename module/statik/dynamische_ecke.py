
""" Eine dynamische Ecke ist eine bewegliche Ecke in einem Statik-Objekt."""

import numpy as np
from matplotlib import path
from . ecke import ecke


class dynamische_ecke(ecke):
    
    
    def __init__(self, position, statik, dynamik, ans_kraft = "DEFAULT"):
        """ Im Statik-Objekt werden alle Kräfte der dynamischen Ecke gespeichert. Es gibt deinen Speicherplatz hierfür in der dynamischen_ecke selbst.
        """
        
        super().__init__(position)
        self.masse = 1
        self.beschleunigung = np.zeros(len(position))
        self.geschwindigkeit = np.zeros(len(position))
        
        self.mikro_beschleunigung = np.zeros(len(position))
        self.mikro_geschwindigkeit = np.zeros(len(position))
        
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
    
        # Trenne noch die Geschwindigkeit für große Bewegungen von Geschwindigkeiten kleiner Bewegungen.
        self.beschleunigung = self.res_kraft / self.masse
        self.geschwindigkeit += self.beschleunigung * zeitänderung
        self.position += self.geschwindigkeit * zeitänderung
        
        dynamik.kanten_real |= {k.berechne_reale_kraft for k in self.kanten}
        dynamik.ecken_update.add(self.update)
        if (sum(self.mikro_geschwindigkeit**2) >= (0.01 / self.masse * zeitänderung)**2).any():
            dynamik.ecken_bewege.add(self.bewege)
    
    def update(self, dynamik, zeitänderung, fe_support):
        """ Passt die Geschwindigkeit und die Position an.
            Fügt den zukünftigen Events die eigene Update-Methode und die Update-Methode der Kanten hinzu."""
        
        # Schritt 1: Berechne die neuen Werte
        
        # Bewegung
        self.mikro_beschleunigung = (self.wirkende_kraft(fe_support)) / self.masse
        
        # Modifizierung für schnellere Konvergenz
        #if (sum(self.geschwindigkeit * self.beschleunigung)**2 ) >= (sum(self.beschleunigung **2) * sum(self.geschwindigkeit **2)) * 0.95:
        #    self.geschwindigkeit *= 1.04
        #if (sum(self.geschwindigkeit * self.beschleunigung) ) <= - np.sqrt((sum(self.beschleunigung **2) * sum(self.geschwindigkeit **2)) * 0.9):
        #    self.geschwindigkeit *= 0.98
        self.mikro_geschwindigkeit *= 0.985
        
        if np.linalg.norm(self.mikro_beschleunigung * self.masse) >= 1:
            self.mikro_geschwindigkeit *= 0.9
            
        self.mikro_geschwindigkeit += self.mikro_beschleunigung * zeitänderung
        self.position += self.mikro_geschwindigkeit * zeitänderung #* np.sqrt(1 + 3*max(sum(alte_beschleunigung * self.beschleunigung) / sum(self.beschleunigung**2), 3)
        
        
        # Versetzung für schnellere Konvergenz
        versetzung = (self.mikro_beschleunigung * zeitänderung) * zeitänderung
        versetzung = np.minimum(np.maximum(versetzung, -0.2), 0.2)
        self.position += versetzung
        
        #Schritt 2: Stelle sicher, dass bei Bedarf weitere Updates der Ecke und ihrer Kanten durchgeführt werden.
        if (sum(self.mikro_beschleunigung**2) >= (0.01 / self.masse)**2).any() or (sum(self.mikro_geschwindigkeit**2) >= (0.01 / self.masse * zeitänderung)**2).any():
            dynamik.kanten_real |= {k.berechne_reale_kraft for k in self.kanten}
            dynamik.ecken_update.add(self.update)
            
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
    def träge_kraft(self):
        print("Res_Kraft: " + str(self.res_kraft))
        return self.reale_kraft - self.res_kraft
    
    @property
    def reale_kraft(self):
        return sum([k.reale_kraft * self.richtung_von(k.gib_nachbar(self)) for k in self.kanten]) + self.ans_kraft
    
    def wirkende_kraft(self, fe_support):
        return sum([k.wirkende_kraft(fe_support) * self.richtung_von(k.gib_nachbar(self)) for k in self.kanten]) + (1 - fe_support) * self.ans_kraft

    def __str__(self):
        return (super().__str__()
                + "\n Masse : " + str(self.masse)
                + "\n Ansetzende Kraft: " + str(self.ansetzende_kraft)
                + "\n Resultierende Kraft: " + str(self.resultierende_kraft))
