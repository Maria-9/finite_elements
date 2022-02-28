
from ..statik.statik import statik
from ..statik.matplot import matplot
from ..statik.dynamische_ecke import dynamische_ecke
from ..statik.statische_ecke import statische_ecke
from ..statik.kante import kante
import messagebox as msg

    
class universum1:
    
    def __init__(self):
        höhe_turm = 5
        länge_überhang = 2
        num_ecken = 2*(höhe_turm + länge_überhang) + 1
        num_kanten = 2 * num_ecken 
        #self.stat = statik(num_ecken, num_kanten) # Je genauer die Werte für num sind, desto weniger Rechenzeit wird zum Aufbau benötigt.
        self.stat = statik(1, 1)
        self.st_ecken = list()
        self.ecken = list()
        self.kanten = list()
        self.mplot = matplot()
        
        #baue den Turm
        for i in range(höhe_turm*2):
            if i % 2 == 0:
                e = dynamische_ecke((1, i / 2 + 1), self.stat)
            else:
                e = dynamische_ecke((2, (i+1) / 2), self.stat)
            self.ecken.append(e)
        
        #setze Eckpunkt
        self.ecken.append(dynamische_ecke((2, höhe_turm + 1), self.stat))
        
        #baue nach rechts
        for i in range(2*länge_überhang):
            if i % 2 == 0:
                e = dynamische_ecke((3 + i/2, höhe_turm), self.stat)
            else:
                e = dynamische_ecke((2 + (i+1)/2, höhe_turm + 1), self.stat)
            self.ecken.append(e)
        
        #baue den Balancierpunkt für eine Wage
        self.ecken.append(dynamische_ecke((3 + länge_überhang, höhe_turm+1), self.stat))
        self.ecken.append(dynamische_ecke((3 + länge_überhang, höhe_turm+2), self.stat))
        
        #setze zwei statischen Ecken am Boden
        prev_2 = statische_ecke((1, 0))
        prev_1 = statische_ecke((2, 0))
        
        self.st_ecken.extend([prev_2, prev_1])
        
        #setze die Kanten
        for e in self.ecken:
            
            self.kanten.append(kante(prev_2, e, self.stat))
            self.kanten.append(kante(prev_1, e, self.stat))
            
            prev_2 = prev_1
            prev_1 = e
        
        # baue die Wage
        self.ecken.append(dynamische_ecke((1 + länge_überhang, höhe_turm+3), self.stat))
        self.ecken.append(dynamische_ecke((5 + länge_überhang, höhe_turm+3), self.stat))
        self.ecken.append(dynamische_ecke((5 + länge_überhang, höhe_turm+4), self.stat))
        
        self.kanten.append(kante(self.ecken[-4], self.ecken[-3], self.stat))
        self.kanten.append(kante(self.ecken[-4], self.ecken[-2], self.stat))
        self.kanten.append(kante(self.ecken[-2], self.ecken[-3], self.stat))
        self.kanten.append(kante(self.ecken[-1], self.ecken[-2], self.stat))

        
    def plot(self):
        
        for obj in [self.ecken, self.st_ecken, self.kanten]:
            self.mplot.add(obj)
        
        self.mplot.show()

    
    def run(self):
        self.stat.berechne()
        self.plot()