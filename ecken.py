
# Elementare Klassen der Finiten Elemente Analyse

import numpy as np

class ecke:

    # __slots__ = ['nummer', 'dynamisch', 'position', 'ansetzende_kraft', 'resultierende_kraft', 'masse', kanten', 'nachbarn']
    
    _freie_nummern = list()
    _höchste_nummer = 0
    
    @classmethod
    def _neue_nummer(cls):
        if len(cls._freie_nummern) == 0:
            cls._höchste_nummer += 1
            return cls._höchste_nummer - 1
        else:
            return cls._freie_nummern.pop()
            
    
    def __init__(self, position, nummer, dynamisch):
        self.nummer = nummer
        self.dynamisch = dynamisch
        self.position = position
        self.kanten = list()
        self.nachbarn = list()
    
    def __del__(self):
        type(self)._freie_nummern.append(self.nummer)
    
    
    def aktualisiere_strukturmatrix():
        print("noch nicht implementiert")
    
    def __str__(self):
        return ("----------------------------"
                + "\n Nummer: " + str(self.nummer) + ("\t[dynamisch]" if self.dynamisch else "\t[statisch]")
                + "\n Position: " + str(self.position)
                + "\n Kanten : " + str([k.nummer for k in self.kanten])
                + "\n Nachbarn : " + str([n.nummer for n in self.nachbarn]))


class dynamische_ecke(ecke):
    
    def __init__(self, position, masse):
        self.masse = masse
        self.ansetzende_kraft = 0
        self.resultierende_kraft = 0
        super().__init__(position, dynamische_ecke._neue_nummer(), True)
        
    
    def __str__(self):
        return (super().__str__()
                + "\n Masse : " + str(self.masse)
                + "\n Ansetzende Kraft: " + str(self.ansetzende_kraft)
                + "\n Resultierende Kraft: " + str(self.resultierende_kraft))
    

class statische_ecke(ecke):
    
    def __init__(self, position):
        super().__init__(position, statische_ecke._neue_nummer(), False)
    
    
if __name__ == "__main__":
    e = dynamische_ecke(tuple([2, 3]), 4)
    print(e)
    print(e.__repr__())
    d = dynamische_ecke(tuple([2, 4]), 4)
    print(d)
    
    c = statische_ecke(tuple([8,9]))
    print(c)
    
    d = e
    f = dynamische_ecke(tuple([2, 2]), 4)
    print(f)