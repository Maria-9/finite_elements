
""" Ein Objekt dieser Klasse enthält alle Daten, die von der Physik-Klasse im allgemeinen benötigt werden. Spezielle Datenstrukturen, die lediglich
    von einzelnen Aufgabenbereichen benötigt werden, sind in den für sie vorgesehenen Klassenobjekten vorhanden. 
"""
import numpy as np
from .nummeriert import nummeriert
from .dynamische_ecke import dynamische_ecke
from .statische_ecke import statische_ecke
from .kante import kante
from .physik import physik

class sphäre:

    def __init__(self, num_ecken, num_kanten):
        """ num_ecken : Die Anzahl der dynamischen Ecken. """
        self.dim = 2
        self.statische_ecken = dict()       # Nummer -> Element
        self.dynamische_ecken = dict()      # Nummer -> Element
        self.kanten = dict()                # Nummer -> Element
        

        self.stat_ecken_pos = np.zeros(0)
        
        self.ecken_ans = np.zeros(num_ecken*self.dim)
        self.ecken_res = np.zeros(num_ecken*self.dim)
        self.ecken_pos = np.zeros(num_ecken*self.dim)
        
        self.ecken_geschwindigkeit = np.zeros(num_ecken*self.dim)
        self.ecken_beschleunigung = np.zeros(num_ecken*self.dim)
        self.ecken_masse = np.zeros(num_ecken)
        
        self.kanten_res = np.zeros(num_kanten)
        
        self.kanten_natürliche_länge = np.zeros(num_kanten)
        self.kanten_elastizitätsmodul = np.zeros(num_kanten)
        self.kanten_real = np.zeros(num_kanten)               # Die durch Dehnung/Stauchung entstehende Kraft.
        self.kanten_kraft_limit = np.zeros(num_kanten * 2)    # VORSICHT: [Zug-Limit, Druck-Limit] = [-a, b] für a, b > 0

        
        self.physik = physik(self, num_ecken, num_kanten)
    
    def inkludiere(self, obj : nummeriert):
    
        if obj.nummeriert_als(kante):
            self.__inkludiere_kante(obj)
            self.physik.statik.inkludiere_kante(obj)
        
        elif obj.nummeriert_als(dynamische_ecke):
            self.__inkludiere_dyn_ecke(obj)
            
        elif obj.nummeriert_als(statische_ecke):
            self.__inkludiere_stat_ecke(obj)

    def __inkludiere_dyn_ecke(self, dyn_ecke):
        """ inkludiere eine dynamische Ecke """
        
        # stelle sicher, dass genug Speicherplatz für die Kräfte der Ecke vorhanden ist.
        if len(self.ecken_ans) < (dyn_ecke.nummer + 1) * self.dim:
        
            supplement = np.zeros((self.dim*(dyn_ecke.nummer+1) - len(self.ecken_ans),))
            for attr in ['ecken_ans', 'ecken_res', 'ecken_pos', 'ecken_geschwindigkeit', 'ecken_beschleunigung']:
                setattr(self, attr, np.concatenate((getattr(self, attr), supplement)))
            
            # Dies ist gleichbedeutend mit:         (Auskommentierter Code kann gelöscht werden, sobald die obige Zeile funktioniert.)
            # erweitere = lambda array : np.concatenate((array, supplement))
            # self.ecken_ans = erweitere(self.ecken_ans)
            # self.ecken_res = erweitere(self.ecken_res)
            # self.ecken_pos = erweitere(self.ecken_pos)
            # self.ecken_geschwindigkeit = erweitere(self.ecken_geschwindigkeit)
            # self.ecken_beschleunigung = erweitere(self.ecken_beschleunigung)
            
            supplement = np.zeros(dyn_ecke.nummer + 1 - len(self.ecken_masse))
            self.ecken_masse = np.concatenate((self.ecken_masse, supplement))

        # prüfe ob der Speicherplatz anderweitig noch in Verwendung ist.
        else:
            for array in [self.ecken_ans, self.ecken_res, self.ecken_pos, self.ecken_geschwindigkeit, self.ecken_beschleunigung]:
                if (np.array(array[dyn_ecke.nummer*self.dim : (dyn_ecke.nummer+1)*self.dim]) != [0]*self.dim).any():
                    msg.warning("Der Speicherplatz auf den die neu inkludierte Ecke mit Nummer " + str(dyn_ecke.nummer) + " zugreift war ungleich 0.")
                    
        self.dynamische_ecken[dyn_ecke.nummer] = dyn_ecke

    def __inkludiere_stat_ecke(self, stat_ecke):
        """ inkludiere eine statische Ecke """
        
        # stelle sicher, dass genug Speicherplatz für die Positionen der Ecke vorhanden ist.
        if len(self.stat_ecken_pos) < (stat_ecke.nummer + 1) * self.dim:

            supplement = np.zeros((stat_ecke.nummer+1)*self.dim - len(self.stat_ecken_pos))
            self.stat_ecken_pos = np.concatenate((self.stat_ecken_pos, supplement))

        # prüfe ob der Speicherplatz anderweitig noch in Verwendung ist.
        else:
            if (np.array(self.stat_ecken_pos[stat_ecke.nummer*self.dim : (stat_ecke.nummer+1)*self.dim]) != [0]*self.dim).any():
                msg.warning("Der Speicherplatz auf den die neu inkludierte statische Ecke mit Nummer " + str(stat_ecke.nummer) + " zugreift war ungleich 0.")
        
        self.statische_ecken[stat_ecke.nummer] = stat_ecke

    def __inkludiere_kante(self, kante):
    
        if len(self.kanten_res) <= kante.nummer:
            # erweitere die Plätze für die Kantenkräfte
            supplement = np.zeros(kante.nummer - len(self.kanten_res) + 1)
            
            for attr in ['kanten_res', 'kanten_natürliche_länge', 'kanten_elastizitätsmodul', 'kanten_real']:
                setattr(self, attr, np.concatenate((getattr(self, attr), supplement)))
            
            self.kanten_kraft_limit = np.concatenate((self.kanten_kraft_limit, supplement, supplement))
        
        elif self.kanten_res[kante.nummer] != 0 or self.kanten_elastizitätsmodul[kante.nummer] != 0:
            msg.warning("Der Speicherplatz auf den die neue Kante mit Nummer " + str(kante.nummer) + " zugreift war ungleich 0.")
        
        self.kanten[kante.nummer] = kante

    def exkludiere(self, obj : nummeriert):

        if obj.nummeriert_als(kante):
            self.__exkludiere_kante(obj)
            self.physik.statik.exkludiere_kante(obj)
        
        elif obj.nummeriert_als(dynamische_ecke):
            self.__exkludiere_dyn_ecke(obj)
            
        elif obj.nummeriert_als(statische_ecke):
            self.__exkludiere_stat_ecke(obj)
    
    def __exkludiere_stat_ecke(self, stat_ecke):
        self.stat_ecken_pos[stat_ecke.nummer : (stat_ecke.nummer + 1) * self.dim] = [0] * self.dim
        
        del self.statische_ecken[stat_ecke.nummer]
    
    def __exkludiere_dyn_ecke(self, dyn_ecke):
        i = [dyn_ecke.nummer * self.dim + i for i in range(self.dim)]
        
        for attr in [self.ecken_ans, self.ecken_res, self.ecken_pos, self.ecken_geschwindigkeit, self.ecken_beschleunigung]:
            attr[i] = [0] * self.dim
            
        self.ecken_masse[dyn_ecke.nummer] = 0
        
        del self.dynamische_ecken[dyn_ecke.nummer]
    
    def __exkludiere_kante(self, kante):
    
        for attr in [self.kanten_res, self.kanten_natürliche_länge, self.kanten_elastizitätsmodul, self.kanten_real]:
            attr[kante.nummer] = 0
        
        self.kanten_kraft_limit[2*kante.nummer : 2*(kante.nummer + 1)] = [0, 0]
        
        del self.kanten[kante.nummer]



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