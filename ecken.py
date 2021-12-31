
# Elementare Klassen der Finiten Elemente Analyse

import numpy as np

class ecke:
    
    def __init__(self, position, masse, nummer, dynamisch):
        self.nummer = nummer
        self.dynamisch = dynamisch
        self.position = position
        self.ansetzende_kraft = 0
        self.resultierende_kraft = 0
        self.masse = masse
        self.kanten_nachbarn = [] # Im Format: [[Kante, Nachbar], ...]
    
    def aktualisiere_strukturmatrix():
        print("noch nicht implementiert")
    
    def __str__(self):
        return (" Nummer: " + str(self.nummer) + ("\t[dynamisch]" if self.dynamisch else "\[statisch]")
                + "\n Position: " + str(self.position)
                + "\n Ansetzende Kraft: " + str(self.ansetzende_kraft)
                + "\n Resultierende Kraft: " + str(self.resultierende_kraft)
                + "\n Masse : " + str(self.masse))
                # + "\n Nachbarn : " + (str(self.kanten_nachbarn[:][1].nummer) if dim(self.kanten_nachbarn) == 2 else str(self.kanten_nachbarn[:][1].nummer))) 


if __name__ == "__main__":
    e = ecke(tuple([2, 3]), 4, 5, True)
    print(e)