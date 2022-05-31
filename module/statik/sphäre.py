
""" Ein Objekt dieser Klasse enthält alle Daten, die von der Physik-Klasse im allgemeinen benötigt werden. Spezielle Datenstrukturen, die lediglich
    von einzelnen Aufgabenbereichen benötigt werden, sind in den für sie vorgesehenen Klassenobjekten vorhanden. 
"""

from .physik import physik

class sphäre:
    
    def __init__(self):
        self.dim = 2
        self.statische_ecken = dict()       # Nummer -> Element
        self.dynamische_ecken = dict()      # Nummer -> Element
        self.kanten = dict()                # Nummer -> Element
        
        self.stat_ecken_pos = []
        
        self.ecken_pos = []
        self.ecken_res = []
        self.ecken_ans = []
        
        self.ecken_geschwindigkeit = []
        self.ecken_beschleunigung = []
        self.ecken_masse = []
    
        self.kanten_res = []
        
        self.kanten_natürliche_länge = []
        self.kanten_kraft_limit = []
        self.kanten_elastizitätsmodul = []
        
        self.physik = physik()
    
    def inkludiere(self, obj : nummeriert):
    
        if obj.nummeriert_als(kante):
            pass
        elif obj.nummeriert_als(dynamische_ecke):
            pass
        elif obj.nummeriert_als(statische_ecke):
            pass


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