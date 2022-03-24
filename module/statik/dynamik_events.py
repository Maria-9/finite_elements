

class dynamik_events:
    
    def __init__(self, zukünftige_events):
        self.kanten_real = set()
        self.ecken_update = set()
        
        self.zukünftige_events = zukünftige_events
    
    def durchlaufe_events(self, zeitänderung):
        # Ermittle die veränderten Kräfte der Kanten:
        for func in self.kanten_real:
            func(self)
        
        # Ermittle die veränderten Kräfte die auf die eine einzelne Ecke wirken und
        # Verändere die Positionen, Beschleunigung und Geschwindigkeit der entsprechenden Ecken:
        for func in self.ecken_update:
            func(self.zukünftige_events, zeitänderung)
    
    def clear(self):
        self.kanten_real = set()
        self.ecken_update = set()