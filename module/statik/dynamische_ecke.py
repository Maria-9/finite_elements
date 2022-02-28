
""" Eine dynamische Ecke ist eine bewegliche Ecke in einem Statik-Objekt."""

import numpy as np
from matplotlib import path
from . ecke import ecke


class dynamische_ecke(ecke):
    
    
    def __init__(self, position, statik, ans_kraft = "DEFAULT"):
        """ Im Statik-Objekt werden alle Kräfte der dynamischen Ecke gespeichert. Es gibt deinen Speicherplatz hierfür in der dynamischen_ecke selbst.
        """
        if ans_kraft == "DEFAULT":
            ans_kraft = [0 for i in position[0:-1]] + [-1]
            
        
        super().__init__(position)
        self.masse = None # Die Masse spielt erst bei Bewegungen eine Rolle
        
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
        
    def __str__(self):
        return (super().__str__()
                + "\n Masse : " + str(self.masse)
                + "\n Ansetzende Kraft: " + str(self.ansetzende_kraft)
                + "\n Resultierende Kraft: " + str(self.resultierende_kraft))
    
    '''def verts_codes_color(self):
        """ Gibt die Vertexe und Kodes für das plotten mit Matplotlib zurück."""
    
        # verts, codes für den Punkt
        verts, codes = self.verts_codes()
        
        #verts, codes für den Pfeil
        länge_pfeil = 0.5
        norm = np.linalg.norm(self.res_kraft)
        if  norm > 0.05:
            scal = self.res_kraft/norm
            verts.append(self.position)
            verts.append(self.position + scal * länge_pfeil)
            verts.append(self.position + (scal * 0.8 + np.array([scal[1], -scal[0]])*0.2) * länge_pfeil)
            verts.append(self.position + scal * länge_pfeil)
            verts.append(self.position + (scal * 0.8 + np.array([-scal[1], scal[0]])*0.2) * länge_pfeil)
            
            
            codes.append(path.Path.MOVETO)
            codes.append(path.Path.LINETO)
            codes.append(path.Path.MOVETO)
            codes.append(path.Path.LINETO)
            codes.append(path.Path.LINETO)
        
        color = (0, 1 - 1/(np.linalg.norm(self.res_kraft) + 1), 0.1)
        
        return verts, codes, color'''