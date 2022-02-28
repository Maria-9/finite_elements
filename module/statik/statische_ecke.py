
""" Eine Statische Ecke ist ein Fixpunkt im Graphen der Finiten Elemente-Methode. """

from .ecke import ecke 

class statische_ecke(ecke):
    # statische Ecken tragen sich nicht in der statik ein.
    # statische Ecken dienen lediglich als Fixpunkte.
    
    def __init__(self, position):
        super().__init__(position)
    
    def verts_codes_color(self):
        """ Gibt die Vertexe und Kodes für das plotten mit Matplotlib zurück."""
        verts, codes = self.verts_codes()
        
        color = (0, 0, 0)

        return verts, codes, color

