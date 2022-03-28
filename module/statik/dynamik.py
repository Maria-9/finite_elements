
""" Dynamik...
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
            
            
        