
""" Eine Statische Ecke ist ein Fixpunkt im Graphen der Finiten Elemente-Methode. """

from .ecke import ecke 

class statische_ecke(ecke):
    # statische Ecken tragen sich nicht in der statik ein.
    # statische Ecken dienen lediglich als Fixpunkte.
    
    def __init__(self, position):
        super().__init__(position)


