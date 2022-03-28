
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
        self.aktuelle_events.durchlaufe_events(zeitänderung, fe_support)
        
        self.aktuelle_events.zukünftige_events.kanten_res |= self.aktuelle_events.kanten_res
        self.aktuelle_events = self.aktuelle_events.zukünftige_events
        self.aktuelle_events.zukünftige_events = dynamik_events(None)
    
    def setze_kanten_res(self):
        self.aktuelle_events.setze_kanten_res()
    
    def inkludiere(self, obj):
        # Da die Nummerierung eigentlich für die statik-Klasse gedacht war, ist die Frage ob es nicht schöner wäre eine eigene Funktion als Typprüfung zu verwenden.
        if isinstance(obj, kante):
            self.aktuelle_events.kanten_real.add(obj.berechne_reale_kraft)
        elif isinstance(obj, dynamische_ecke):
            self.aktuelle_events.ecken_update.add(obj.update)
        elif isinstance(obj, statische_ecke):
            pass
        else:
            msg.info("Objekt konnte nicht in die Dynamik inkludiert werden.")
    
    def exkludiere(self, obj):
        # Ev. wird diese Funktion nicht benötigt.
        if isinstance(obj, kante):
            self.aktuelle_events.kanten_real - {obj.berechne_reale_kraft}
        elif isinstance(obj, dynamische_ecke):
            self.aktuelle_events.ecken_update - {obj.update}
        elif isinstance(obj, statische_ecke):
            pass
        else:
            msg.info("Objekt konnte nicht aus der Dynamik exkludiert werden.")
            
            
        