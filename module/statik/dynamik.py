
""" Dynamik --- dieses Modul wird in Zukunft neu geschrieben oder überarbeitet werden, sobald eine dynamik mit Objekten implementiert wird.

    Bis dato steht diese Klasse auf dem Eis.
"""

"""
NOTIZEN AUS DEM MODUL KANTEN-MODUL
----------------------------------

def kraft_zu_länge(self, kraft):
        ''' Umkehrfunktion zu 'berechne_reale_kraft' '''
        return (self.natürliche_länge / (1 + kraft / self.elastizitätsmodul))^2
    
    def berechne_reale_kraft(self, dynamik, tol = 1):
        # Die Toleranz 'tol' gibt an, ab wann die Differenz zwischen der realen Kraft und
        # der aus der aktuellen Stauchung der Kante entstehenden Kraft klein genug ist, damit die reale Kraft nicht angepasst wird.
        # Hierzu wird diese Toleranz erst durch den Elastizitätsmodul und die natürliche Länge der Kante geteilt.
        
        aktuelle_länge = np.linalg.norm(self.ecke1.position - self.ecke2.position)
        
        # Im wesentlichen ist eine Differentialgleichung gegeben:
        #   l'(f) = (f * l(f)^2) / (V * E)  , wobei
        #   l(f) Die Länge des Stabes bei einwirkender Kraft f ist
        #   V das Volumen des Stabes, und
        #   E das Elastizitätsmodul
        #
        # Wofram Alpha schlägt als Lösung f = sqrt( 2*E*V*(1 - L/l) ) vor, dies entspricht in etwa der Wurzel des obigen antiproportionalen Verhältnisses.
        # Nehmen wir an, dass das Volumen eines Stabes proportional zu seiner Länge zunimmt ergeben sich die folgenden Gleichungen.
        # Es ist denkbar die Wurzel zu Vernachlässigen, um bessere Performance zu erzielen.
        
        antiprop = self.elastizitätsmodul * self.natürliche_länge * (self.natürliche_länge / aktuelle_länge - 1)

        neue_reale_kraft = math.sqrt(antiprop)
        
        ''' Dies wird lediglich für Bewegungen benötigt.
        
        if abs(self.__reale_kraft - neue_reale_kraft) > tol / (self.elastizitätsmodul * self.natürliche_länge):
            self.__reale_kraft = neue_reale_kraft
            dynamik.kanten_rev.add(self.revidiere_statik)
            dynamik.ecken_update.add(self.ecke1.update)
            dynamik.ecken_update.add(self.ecke2.update)
        '''
        
        return self.__reale_kraft
    
    def revidiere_statik(self):
        self.setze_res_kraft = self.__reale_kraft
        self.statik.revidiere(self)
--------------------------------------------
"""
    
from .kante import kante
from .dynamische_ecke import dynamische_ecke
from .statische_ecke import statische_ecke

class dynamik:
    
    def __init__(self):
        self.kanten_real = set()
        self.ecken_update = set()
        self.kanten_rev = set()
        
        self.ecken_bewege = set()
    
    def durchlaufe_events(self, zeitänderung, fe_support=0):
        """ Durchlaufe die aktuellen Events mit Außnahme der Kanten Revidierungen für die Statik."""
        
        # Speichere die Events in separaten Mengen und 'Resette' die alten Events.
        alt_kanten_real, self.kanten_real = self.kanten_real, set()
        alt_ecken_update, self.ecken_update = self.ecken_update, set()
        
        # Ermittle die veränderten Kräfte der Kanten:
        while len(alt_kanten_real) > 0:
            alt_kanten_real.pop()(self)
        
        # Ermittle die veränderten Kräfte die auf die eine einzelne Ecke wirken und
        # Verändere die Positionen, Beschleunigung und Geschwindigkeit der entsprechenden Ecken:
        while len(alt_ecken_update) > 0:
            alt_ecken_update.pop()(self, zeitänderung, fe_support)
    
    def rev_kanten_stat(self):
        """ Revidiere die Einträge in der Statik, die alle veränderten Kanten betreffen."""
        while(len(self.kanten_rev) > 0):
            self.kanten_rev.pop()()
    
    def bewege_ecken(self, zeitänderung):
        alt_ecken_bewege, self.ecken_bewege = self.ecken_bewege, set()
        while(len(alt_ecken_bewege) > 0):
            alt_ecken_bewege.pop()(self, zeitänderung)
    
    def inkludiere(self, obj):
        """ Nehme das Objekt 'obj' in die Routine der Events auf. """
        if isinstance(obj, kante):
            self.kanten_real.add(obj.berechne_reale_kraft)
        elif isinstance(obj, dynamische_ecke):
            self.ecken_update.add(obj.update)
            self.ecken_bewege.add(obj.bewege)
        elif isinstance(obj, statische_ecke):
            pass
        else:
            msg.info("Objekt konnte nicht in die Dynamik inkludiert werden.")
    
    def exkludiere(self, obj):
        """ Nehme das Objekt aus der Routine der Events heraus. Man bemerke, dass ein Objekt selbst verschwindet,
            wenn es keine weiteren Veränderungen erfährt."""
        if isinstance(obj, kante):
            self.kanten_real - {obj.berechne_reale_kraft}
        elif isinstance(obj, dynamische_ecke):
            self.ecken_update - {obj.update}
            self.ecken_bewege - {obj.bewege}
        elif isinstance(obj, statische_ecke):
            pass
        else:
            msg.info("Objekt konnte nicht aus der Dynamik exkludiert werden.")
            
            
        