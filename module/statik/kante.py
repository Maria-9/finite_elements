
""" Eine Kante stellt die Kante im Graphen einer Finiten-Elemente Analyse dar."""

from matplotlib import path
from .nummeriert import nummeriert

class kante(nummeriert):

    def __init__(self, ecke1, ecke2, statik, kraft_limit=28):
        
        super().__init__()
        self.kraft_limit = kraft_limit

        self.ecke1 = ecke1
        self.ecke2 = ecke2

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
        
    def __del__(self):
        msg.info("Shall I get deleted?")
        self.statik.exkludiere(self)
        super().__del__()
          
    def __str__(self):
        return (super().__str__()
                + "\n Ecken: [" + str(self.ecke1.nummer) + ", " + str(self.ecke2.nummer) + "]")
            
    '''def verts_codes_color(self):
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
        
        return (verts, codes, color)'''