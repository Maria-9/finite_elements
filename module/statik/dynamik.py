
""" Dynamik...
"""

from .dynamik_events import dynamik_events
from .kante import kante
from .dynamische_ecke import dynamische_ecke
from .statische_ecke import statische_ecke

class dynamik:
    
    def __init__(self):
        self.aktuelle_events = dynamik_events(dynamik_events(None))
    
    def durchlaufe_events(self, zeitänderung, fe_support=0):
        """ Durchlaufe die aktuellen Events und übertrage die Kanten_revidierungs-Events in den nächsten Schritt."""
        self.aktuelle_events.durchlaufe_events(zeitänderung, fe_support)
        
        self.aktuelle_events.zukünftige_events.kanten_rev |= self.aktuelle_events.kanten_rev
        self.aktuelle_events = self.aktuelle_events.zukünftige_events
        self.aktuelle_events.zukünftige_events = dynamik_events(None)
    
    def rev_kanten_stat(self):
        """ Revidiere die Einträge in der Statik, die alle veränderten Kanten betreffen."""
        self.aktuelle_events.rev_kanten_stat()
    
    def inkludiere(self, obj):
        """ Nehme das Objekt 'obj' in die Routine der dynamischen_events auf. """
        if isinstance(obj, kante):
            self.aktuelle_events.kanten_real.add(obj.berechne_reale_kraft)
        elif isinstance(obj, dynamische_ecke):
            self.aktuelle_events.ecken_update.add(obj.update)
        elif isinstance(obj, statische_ecke):
            pass
        else:
            msg.info("Objekt konnte nicht in die Dynamik inkludiert werden.")
    
    def exkludiere(self, obj):
        """ Nehme das Objekt aus der Routine der dynamischen_events heraus. Man merke, dass sich ein Objekt selbst verschwindet,
            wenn es keine weiteren Veränderungen erfährt."""
        if isinstance(obj, kante):
            self.aktuelle_events.kanten_real - {obj.berechne_reale_kraft}
        elif isinstance(obj, dynamische_ecke):
            self.aktuelle_events.ecken_update - {obj.update}
        elif isinstance(obj, statische_ecke):
            pass
        else:
            msg.info("Objekt konnte nicht aus der Dynamik exkludiert werden.")
            
            
        