
import numpy as np
import matplotlib.path as path
import math

from .ecke import ecke
from .dynamische_ecke import dynamische_ecke
from .statische_ecke import statische_ecke
from .kante import kante


class p_ecke(ecke):
    __class__ = ecke
    def verts_codes_color(self, size = 0.1):
        """ Gibt die Listen von Vertexes und Codes für das Plotten der Ecke mit Matplotlib zurück. """
        if self.dim != 2:
            raise Exception("Diese Funktion ist nur für 2-D Plots erstellt worden.")
    
        verts = [self.position + np.array([1, 0])*size,
                self.position + np.array([0, 1])*size,
                self.position + np.array([-1, 0])*size,
                self.position + np.array([0, -1])*size,
                self.position + np.array([1, 0])*size]

        codes = [path.Path.MOVETO,
                path.Path.LINETO,
                path.Path.LINETO,
                path.Path.LINETO,
                path.Path.CLOSEPOLY]

        return (verts, codes, (0, 0, 0))


class p_dynamische_ecke(dynamische_ecke, p_ecke):
    __class__ = dynamische_ecke
    
    def __init__(self, position, *args):
        dynamische_ecke.__init__(self, position, *args)
        # Da 'p_ecke' lediglich den Konstruktor von 'ecke' verwendet, der wiederum von der dynamischen_ecke aufgerufen wird,
        # kann,sollte und wird auf den Konstruktor von 'p_ecke' verzichtet.
        print(self)
    
    def verts_codes_color(self):
        """ Gibt die Vertexe und Kodes für das plotten mit Matplotlib zurück."""
    
        # verts, codes für den Punkt
        verts, codes, color = super().verts_codes_color()
        
        #verts, codes für den Pfeil
        kraft = self.res_kraft
        norm = np.linalg.norm(kraft)
        #print(norm)
        länge_pfeil = 0.7 * norm * 10
        if  True:
            scal = kraft/norm
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
        
        color = (0, 1 - 1/(np.linalg.norm(kraft) + 1), 0.1)
        
        return verts, codes, color


class p_statische_ecke(statische_ecke, p_ecke):
    __class__ = statische_ecke
    def verts_codes_color(self):
        """ Gibt die Vertexe und Kodes für das plotten mit Matplotlib zurück."""
        verts, codes, color = super().verts_codes_color()
        
        color = (0, 0, 0)

        return verts, codes, color


class p_kante(kante):
    __class__ = kante
    
    def __init__(self, ecke1, ecke2, statik, dynamik, darstellung = 0):
        """ darstellung = 0 zeichnet die Linie mittig, höhere Darstellungen zeichnen die Linie neben die Mittellinie."""
        self.darstellung = darstellung
        super().__init__(ecke1, ecke2, statik, dynamik)

    def verts_codes_color(self):
        """ Gibt die Vertexe und Kodes für das plotten mit Matplotlib zurück."""
        if self.sphäre.dim != 2:
            raise Exception("Diese Funktion ist nur für 2-D Plots erstellt worden.")
        
        x = self.ecke1.position - self.ecke2.position
        verschiebung = np.array([x[1], -x[0]])
        verschiebung = verschiebung / np.linalg.norm(verschiebung) * self.darstellung * 0.05
        verts = [self.ecke1.position, self.ecke2.position] + verschiebung
        
        codes = [path.Path.MOVETO,
                path.Path.LINETO]
        
        color = [0, 0, 0] # RGB
        kraft = self.res_kraft
        if kraft > 0:
            color[0] = min(1, kraft / self.kraft_limit)
        else:
            color[2] = min(1, -kraft / self.kraft_limit)
            if kraft < -self.kraft_limit:
                color[1] = 1
        
        return (verts, codes, color)