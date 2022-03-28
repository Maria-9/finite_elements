
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
        self.continuation = 0
        
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
        trä_kraft = self.wirkende_kraft
        bew_kraft = self.bew_kraft
        if sum(trä_kraft**2) <= self.ignorierte_kraft**2:
            kraft = np.array([0.0, 0.0])
        
        # Bewegung
        self.beschleunigung_bew = bew_kraft / self.masse
        alte_beschleunigung = self.beschleunigung
        self.beschleunigung = trä_kraft / self.masse
        #print("----")
        #print(self.beschleunigung)
        #if sum(self.geschwindigkeit * self.beschleunigung) <= 0:
        #    self.geschwindigkeit = [0.0, 0.0]
        if sum(self.geschwindigkeit * self.beschleunigung) >= sum(self.beschleunigung * self.beschleunigung) * zeitänderung and np.linalg.norm(self.geschwindigkeit) <= 2:
            self.geschwindigkeit += self.beschleunigung * zeitänderung * 3
        self.geschwindigkeit += self.beschleunigung * zeitänderung
        self.position += self.geschwindigkeit * zeitänderung #* np.sqrt(1 + 3*max(sum(alte_beschleunigung * self.beschleunigung) / sum(self.beschleunigung**2), 3))
        self.geschwindigkeit *= 0.98
        #else:
        #    self.geschwindigkeit *= 1.02
        #if np.linalg.norm(bew_kraft) >= 0.1:
        #    self.geschwindigkeit *= 0.9 #(1 - 0.2*zeitänderung)   # Dämpfung für realistische Animation
        if np.linalg.norm(self.geschwindigkeit) >= 1:
            self.geschwindigkeit *= 0.5
        
        
        # Versetzung durch die träge Kraft
        if (trä_kraft != np.nan).all():
            #print(trä_kraft)
            versetzung = (trä_kraft / self.masse * zeitänderung) * zeitänderung
            versetzung = np.minimum(np.maximum(versetzung, -2), 2)
            #versetzung = self.geschwindigkeit * zeitänderung * sum(alte_beschleunigung * self.beschleunigung) / sum(self.beschleunigung**2)
            #if sum(alte_beschleunigung * self.beschleunigung) >= sum(self.beschleunigung**2) * 0:
                #self.continuation += 1
                #if self.continuation >= 100:
            #    versetzung += 0.2 * self.geschwindigkeit * zeitänderung
            #else:
            #    self.continuation = 0
            # versetzung = (sum([k.versetzung / 2 * self.richtung_von(k.gib_nachbar(self)) for k in self.kanten])) 
            #print("---" + str(np.linalg.norm(versetzung)))
            self.position += versetzung
        
        # Schritt 2: Setze Werte für die nächste Berechnung der Statik
        # self.setze_res_kraft = self.reale_kraft
        for k in self.kanten:
            k.revidiere_strukturmatrix()
        
        #Schritt 3: Stelle sicher, dass bei Bedarf weitere Updates der Ecke und ihrer Kanten durchgeführt werden.
        if (self.res_kraft != 0).any() or (trä_kraft != 0).any() or (self.beschleunigung != 0).any() or (self.geschwindigkeit != 0).any():
            zukünftige_events.kanten_real |= {k.berechne_reale_kraft for k in self.kanten}
            zukünftige_events.ecken_update.add(self.update)
            # Der Term '(self.res_kraft != 0).any()' sollte in das Statik-Modul verschoben werden.
            
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
    def bew_kraft(self):
        return self.res_kraft
    
    @property
    def reale_kraft(self):
        return sum([k.reale_kraft * self.richtung_von(k.gib_nachbar(self)) for k in self.kanten]) + self.ans_kraft
    
    @property
    def wirkende_kraft(self):
        return sum([k.wirkende_kraft * self.richtung_von(k.gib_nachbar(self)) for k in self.kanten]) + (1 - self.kanten[0].fe_support) * self.ans_kraft

    def __str__(self):
        return (super().__str__()
                + "\n Masse : " + str(self.masse)
                + "\n Ansetzende Kraft: " + str(self.ansetzende_kraft)
                + "\n Resultierende Kraft: " + str(self.resultierende_kraft))
