

class dynamik_events:
    
    def __init__(self, zukünftige_events):
        self.kanten_real = set()
        self.ecken_update = set()
        self.kanten_rev = set()
        
        self.zukünftige_events = zukünftige_events
    
    def durchlaufe_events(self, zeitänderung, fe_support):
        # Ermittle die veränderten Kräfte der Kanten:
        for func in self.kanten_real:
            func(self)
        
        # Ermittle die veränderten Kräfte die auf die eine einzelne Ecke wirken und
        # Verändere die Positionen, Beschleunigung und Geschwindigkeit der entsprechenden Ecken:
        for func in self.ecken_update:
            func(self.zukünftige_events, zeitänderung, fe_support)
    
    def rev_kanten_stat(self):
        while(len(self.kanten_rev) > 0):
            self.kanten_rev.pop()()