
""" Ein Objekt dieser Klasse enthält alle Daten, die von der Physik-Klasse im allgemeinen benötigt werden. Spezielle Datenstrukturen, die lediglich
    von einzelnen Aufgabenbereichen benötigt werden, sind in den für sie vorgesehenen Klassenobjekten vorhanden. 
"""
import numpy as np
from .physik import physik

class sphäre:
    
    def __init__(self, num_ecken, num_kanten):
        """ num_ecken : Die Anzahl der dynamischen Ecken. """
        self.dim = 2
        self.statische_ecken = dict()       # Nummer -> Element
        self.dynamische_ecken = dict()      # Nummer -> Element
        self.kanten = dict()                # Nummer -> Element
        
        self.stat_ecken_pos = np.zeros(0)
        
        self.ecken_pos = np.zeros(num_ecken*self.dim)
        self.ecken_res = np.zeros(num_ecken*self.dim)
        self.ecken_ans = np.zeros(num_ecken*self.dim)
        
        self.ecken_geschwindigkeit = np.zeros(num_ecken*self.dim)
        self.ecken_beschleunigung = np.zeros(num_ecken*self.dim)
        self.ecken_masse = np.zeros(num_ecken)
    
        self.kanten_res = np.zeros(num_kanten)
        
        self.kanten_natürliche_länge = np.zeros(num_kanten)
        self.kanten_kraft_limit = np.zeros(num_kanten * 2)    # VORSICHT: [Zug-Limit, Druck-Limit]
        self.kanten_elastizitätsmodul = np.zeros(num_kanten)
        self.kanten_real = np.zeros(num_kanten)               # Die durch Dehnung/Stauchung entstehende Kraft.
        
        self.physik = physik()
    
    def inkludiere(self, obj : nummeriert):
    
        if obj.nummeriert_als(kante):
            pass
        
        elif obj.nummeriert_als(dynamische_ecke):
            self.__inkludiere_dyn_ecke(obj)
            
        elif obj.nummeriert_als(statische_ecke):
            pass

    def __inkludiere_dyn_ecke(self, dyn_ecke):
        """ inkludiere eine dynamische Ecke """
        
        # stelle sicher, dass es Plätze für die Kräfte der Ecke gibt.
        if len(self.ecken_ans) <= obj.nummer*self.dim:
            supplement = np.zeros((self.dim*(obj.nummer+1) - len(self.ecken_ans),))
                self.sphäre.ecken_ans = np.concatenate((self.sphäre.ecken_ans, supplement))
                self.sphäre.ecken_res = np.concatenate((self.sphäre.ecken_res, supplement))
            else:
                for array in [self.sphäre.ecken_ans, self.sphäre.ecken_res]:
                    if (np.array(array[obj.nummer*self.dim : (obj.nummer+1)*self.dim]) != [0]*self.dim).any():
                        msg.warning("Der Speicherplatz auf den die neue Ecke zugreift war ungleich 0.")
            
            # füge die Bewege- Methode der Ecke hinzu.
            #if obj.nummer in self.ecken_bewege:
            #    msg.warning("Die Bewege- Methode einer Ecke wurde unerwartet durch eine andere Bewegungs- Methode eier anderen ersetzt.")
            #self.ecken_bewege[obj.nummer] = obj.bewege
        
    

"""
    Welcher Bereich der Physik greift auf welche Objekte zu?
    
    Statik:
        Lesend:
            ecken_res
            ecken_ans
            kanten_res
        
        Schreibend:
            ecken_res
            kanten_res
        
        Eigene Datenstruktur:
            strukturmatrix : kanten_res * strukturmatrix  + ecken_ans = ecken_res
"""