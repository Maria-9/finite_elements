
""" Eine dynamische Ecke ist eine bewegliche Ecke in einem Statik-Objekt."""

import numpy as np
from matplotlib import path
from . ecke import ecke


class dynamische_ecke(ecke):
    
    
    def __init__(self, position, statik, dynamik, ans_kraft = "DEFAULT"):
        """ Im Statik-Objekt werden alle Kräfte der dynamischen Ecke gespeichert. Es gibt deinen Speicherplatz hierfür in der dynamischen_ecke selbst.
        """
        
        super().__init__(position)
        self.masse = 0.1 # Die Masse spielt erst bei Bewegungen eine Rolle
        self.beschleunigung = np.zeros(len(position))
        self.geschwindigkeit = np.zeros(len(position))
        self.ignorierte_kraft = 0
        
        if ans_kraft == "DEFAULT":
            ans_kraft = np.array([0 for i in position[0:-1]] + [-1]) * self.masse
        
        self.dynamik = dynamik # Eigentlich sollte dieses Objekt hier nicht weiter benötigt werden.
        self.dynamik.inkludiere(self)
        
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
    
    def update(self, zukünftige_events, zeitänderung):
        # verrechne die Resultierenden Kräfte mit den realen Kräften und passe die Beschleunigung, die Geschwindigkeit und die Position an.
        # Man denke daran, dass bei bestehender Geschwindigkeit, Beschleunigung oder einem Ungleichgewicht der von den Kanten wirkenden realen Kräfte
        # im nächsten Schritt der Animation stets wieder ein Update für diese Ecke durchgeführt werden sollte. Man setzt dies am besten durch einen
        # EventHandler um.
        
        # Schritt 1: Berechne die neuen Werte
        kraft = self.wirkende_kraft
        if sum(kraft**2) <= self.ignorierte_kraft**2:
            kraft = np.array([0.0, 0.0])

         
        self.beschleunigung = kraft / self.masse * 4
        
        if np.linalg.norm(self.beschleunigung) >= 1.5 / self.masse:
            self.beschleunigung *= 0.25
        
        
        self.geschwindigkeit += self.beschleunigung * zeitänderung
        
        if np.linalg.norm(self.geschwindigkeit) >= 0.5:
            self.geschwindigkeit *= 0.1
        
        self.position += self.geschwindigkeit * zeitänderung   
        
        self.geschwindigkeit *= 0.98   # Dämpfung für bessere Konvergenz
        
        
        # Schritt 2: Setze Werte für die nächste Berechnung der Statik
        self.setze_res_kraft = self.reale_kraft
        for k in self.kanten:
            k.revidiere_strukturmatrix()
        
        #Schritt 3: Stelle sicher, dass bei Bedarf weitere Updates der Ecke und ihrer Kanten durchgeführt werden.
        if (kraft != 0).any() or (self.beschleunigung != 0).any() or (self.geschwindigkeit != 0).any():
            zukünftige_events.kanten_real |= {k.berechne_reale_kraft for k in self.kanten}
            zukünftige_events.ecken_update.add(self.update)
    
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
    
    @property
    def wirkende_kraft(self):
        return sum([k.wirkende_kraft * self.richtung_von(k.gib_nachbar(self)) for k in self.kanten]) + self.ans_kraft

    def __str__(self):
        return (super().__str__()
                + "\n Masse : " + str(self.masse)
                + "\n Ansetzende Kraft: " + str(self.ansetzende_kraft)
                + "\n Resultierende Kraft: " + str(self.resultierende_kraft))
