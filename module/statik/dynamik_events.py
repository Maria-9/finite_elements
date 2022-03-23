

class dynamik_events:
    
    def __init__(self, zukünftige_events : dynamik_events):
        self.kanten_real = set()
        self.ecken_real = set()     # Kann diese Menge von Funktionen ausgelassen werden?
        self.ecken_update = set()
        
        self.zukünftige_events = zukünftige_events
    
    def durchlaufe_events(self):
        # Schritt 1: Ermittle die veränderten Kräfte der Kanten:
        for func in self.kanten_real:
            func(self)
        
        # Schritt 2: Ermittle die veränderten Kräfte die auf die Kanten wirken:
        for func in self.ecken_real:
            func(self)
        
        # Schritt 3: Verändere die Positionen der entsprechenden Ecken:
        for func in self.ecken_update:
            func(self, zukünftige_events)
    
    def clear(self):
        self.kanten_real = set()
        self.ecken_real = set()
        self.ecken_update = set()