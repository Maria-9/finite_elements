
""" Ein Eckenobjekt repräsentiert eine Ecke im Graphen einer Finiten Elemente-Methode. """

import numpy as np
from .nummeriert import nummeriert
from matplotlib import path

class ecke(nummeriert):

    # __slots__ = ['nummer', 'dynamisch', 'position', 'ansetzende_kraft', 'resultierende_kraft', 'masse', kanten']
    
    def __init__(self, position):
        super().__init__() # Gebe dem Objekt eine Nummer
        
        self.position = np.array(position)
        self.dim = len(position)
        self.kanten = list()
    
    def __del__(self):
        super().__del__()
    
    def neue_kante(self, kante):

        if kante in self.kanten:
            msg.error("Die Kante " + str(kante) + " ist bereits in der Liste der Kanten der Ecke " + self.nummer + " vorhanden.")
            raise ValueError("Die Kante " + str(kante) + " ist bereits in der Liste der Kanten der Ecke " + self.nummer + " vorhanden.")
        
        self.kanten.append(kante)
    
    def entferne_kante(self, kante):
        self.kanten.remove(kante)
    
    def richtung_von(self, andere_ecke):
        # gibt den Richtungsvektor zurück.
        x = self.position - andere_ecke.position
        return x / np.sqrt(x @ x)
    
    def __str__(self):
        return ("----------------------------"
                + super().__str__() # dies ist die Nummerierung
                + "\n Position: " + str(self.position)
                + "\n Kanten : " + str([k.nummer for k in self.kanten]))


