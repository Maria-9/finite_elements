
""" Ein Eckenobjekt repräsentiert eine Ecke im Graphen einer Finiten Elemente-Methode. """

import numpy as np
from .nummeriert import nummeriert
from matplotlib import path

class ecke(nummeriert):

    # __slots__ = ['nummer', 'dynamisch', 'position', 'ansetzende_kraft', 'resultierende_kraft', 'masse', kanten']
    
    def __init__(self, position):
        super().__init__() # Gebe dem Objekt eine Nummer
        
        self.original_position = np.array(position, dtype=float)
        self.position = np.array(position, dtype=float)
        self.dim = len(position)
        self.kanten = list()
    
    def __del__(self):
        super().__del__()
    
    def delete(self):
        for k in self.kanten:
            k.__del__()
    
    def neue_kante(self, kante):

        if kante in self.kanten:
            msg.error("Die Kante " + str(kante) + " ist bereits in der Liste der Kanten der Ecke " + self.nummer + " vorhanden.")
            raise ValueError("Die Kante " + str(kante) + " ist bereits in der Liste der Kanten der Ecke " + self.nummer + " vorhanden.")
        
        self.kanten.append(kante)
    
    def entferne_kante(self, kante):
        self.kanten.remove(kante)
    
    def richtung_von(self, andere_ecke):
        """ Gibt den Richtungsvektor von der anderen Ecke zu sich selbst zurück. """
        x = self.position - andere_ecke.position
        return x / np.sqrt(x @ x)
    
    def update(self, *args):
        # Diese Funktion wird von der dynamischen Ecke überschrieben, in der statischen Ecke erfüllt sie keinen weiteren Sinn als da zu sein.
        pass
    
    def bewege(self):
        pass
        
    def __str__(self):
        return ("----------------------------"
                + super().__str__() # dies ist die Nummerierung
                + "\n Position: " + str(self.position)
                + "\n Kanten : " + str([k.nummer for k in self.kanten]))


