
import numpy as np
import matplotlib.path as path

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
    def verts_codes_color(self):
        """ Gibt die Vertexe und Kodes für das plotten mit Matplotlib zurück."""
    
        # verts, codes für den Punkt
        verts, codes, color = super().verts_codes_color()
        
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
    def verts_codes_color(self):
        """ Gibt die Vertexe und Kodes für das plotten mit Matplotlib zurück."""
        if self.ecke1.dim != 2 or self.ecke2.dim != 2:
            raise Exception("Diese Funktion ist nur für 2-D Plots erstellt worden.")
        
        verts = [self.ecke1.position, self.ecke2.position]
        
        codes = [path.Path.MOVETO,
                path.Path.LINETO]
        
        color = [0, 0, 0] # RGB
        if self.res_kraft > 0:
            color[0] = min(1, self.res_kraft / self.kraft_limit)
        else:
            color[2] = min(1, -self.res_kraft / self.kraft_limit)
            if self.res_kraft < -self.kraft_limit:
                color[1] = 1
        
        return (verts, codes, color)