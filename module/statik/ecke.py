
""" Ein Eckenobjekt repräsentiert eine Ecke im Graphen einer Finiten Elemente-Methode. """

import numpy as np
from .nummeriert import nummeriert
from matplotlib import path
from abc import ABC, abstactmethod
#from .sphäre import sphäre

class ecke(nummeriert):

    # __slots__ = ['nummer', 'dynamisch', 'position', 'ansetzende_kraft', 'resultierende_kraft', 'masse', kanten']
    
    def __init__(self, sphäre):
        super().__init__() # Gebe dem Objekt eine Nummer
 
        self.sphäre = sphäre
        self.sphäre.inkludiere(self)
        self.kanten = list() # Es erscheint vorerst sinnvoll die Kanten im Objekt zu speichern. Es ist zu Bedenken diese Informationen in der Sphäre zu Speichern.

    @abc.abstractproperty 
    def position(self):
        # Die Position verschiedener Ecktypen (statisch / dynamisch) wird an unterschiedlichen Stellen in der Sphäre gespeichert.
        pass
    
    @property
    def spb(self):
        # 'spb' steht für Speicherbereich
        # Gibt den Speicherbereich der Attribute in der Sphäre zurück.
        return [self.nummer*self.sphäre.dim + i for i in range(self.sphäre.dim)]
    
    @property
    def dim(self):
        return self.sphäre.dim

    def delete(self):
        for k in self.kanten:
            k.delete()
        self.sphäre.exkludiere(self)

    def neue_kante(self, kante):
        if kante in self.kanten:
            msg.error("Die Kante " + str(kante) + " ist bereits in der Liste der Kanten der Ecke " + self.nummer + " vorhanden.")
        self.kanten.append(kante)

    def entferne_kante(self, kante):
        self.kanten.remove(kante)

    def richtung_von(self, andere_ecke):
        """ Gibt den Richtungsvektor von der anderen Ecke zu sich selbst zurück. """
        x = self.position - andere_ecke.position
        return x / np.sqrt(x @ x)

    #def update(self, *args):
         # Diese Funktion wird von der dynamischen Ecke überschrieben, in der statischen Ecke erfüllt sie keinen weiteren Sinn als da zu sein.
    #    pass
    
    #def bewege(self):
    #    pass
        
    def __str__(self):
        return ("----------------------------"
                + super().__str__() # dies ist die Nummerierung
                + "\n Position: " + str(self.position)
                + "\n Kanten : " + str([k.nummer for k in self.kanten]))


