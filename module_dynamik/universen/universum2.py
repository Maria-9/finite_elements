
from ..statik.statik import statik
from ..statik.dynamik import dynamik
from ..statik.matplot import matplot
from ..statik.plotable_inheritances  import p_dynamische_ecke as dynamische_ecke
from ..statik.plotable_inheritances  import p_statische_ecke as statische_ecke
from ..statik.plotable_inheritances  import p_kante as kante
import messagebox as msg
import time
from matplotlib import pyplot as plt
import numpy as np
import time
    
class universum2:
    
    def __init__(self):
        self.höhe_turm = 8
        self.länge_überhang = 8
        höhe_turm = self.höhe_turm
        länge_überhang = self.länge_überhang
        num_ecken = 2*(höhe_turm + länge_überhang) + 1
        num_kanten = 2 * num_ecken 
        #self.stat = statik(num_ecken, num_kanten) # Je genauer die Werte für num sind, desto weniger Rechenzeit wird zum Aufbau benötigt.
        self.stat = statik(1, 1)
        self.st_ecken = list()
        self.ecken = list()
        self.kanten = list()
        self.mplot = matplot()
        
        self.dyn = dynamik()
        
        #baue den Turm
        for i in range(höhe_turm*2):
            if i % 2 == 0:
                e = dynamische_ecke((1, i / 2 + 1), self.stat, self.dyn)
            else:
                e = dynamische_ecke((2, (i+1) / 2), self.stat, self.dyn)
            self.ecken.append(e)
        
        #setze Eckpunkt
        self.ecken.append(dynamische_ecke((2, höhe_turm + 1), self.stat, self.dyn))
        
        #baue nach rechts
        for i in range(2*länge_überhang):
            if i % 2 == 0:
                e = dynamische_ecke((3 + i/2, höhe_turm), self.stat, self.dyn)
            else:
                e = dynamische_ecke((2 + (i+1)/2, höhe_turm + 1), self.stat, self.dyn)
            self.ecken.append(e)
        
        #setze zwei statischen Ecken am Boden
        prev_2 = statische_ecke((1, 0))
        prev_1 = statische_ecke((2, 0))
        
        self.st_ecken.extend([prev_2, prev_1])
        
        #setze die Kanten
        for e in self.ecken:
            
            self.kanten.append(kante(prev_2, e, self.stat, self.dyn))
            self.kanten.append(kante(prev_1, e, self.stat, self.dyn))
            
            prev_2 = prev_1
            prev_1 = e
    
    def next_system(self):
        
        neue_ecken = list()
        # baue den zweiten Turm
        for i in range(self.höhe_turm*2 - 2):
            if i % 2 == 0:
                e = dynamische_ecke((1 + self.länge_überhang, i / 2 + 1), self.stat, self.dyn)
            else:
                e = dynamische_ecke((2 + self.länge_überhang, (i+1) / 2), self.stat, self.dyn)
            neue_ecken.append(e)
        
        #setze zwei statischen Ecken am Boden
        prev_2 = statische_ecke((1 + self.länge_überhang, 0))
        prev_1 = statische_ecke((2 + self.länge_überhang, 0))
        
        self.st_ecken.extend([prev_2, prev_1])
        
        #setze die Kanten des zweiten Turmes
        for e in neue_ecken:
            
            self.kanten.append(kante(prev_2, e, self.stat, self.dyn))
            self.kanten.append(kante(prev_1, e, self.stat, self.dyn))
            
            prev_2 = prev_1
            prev_1 = e
        
        #setze die Verbindungskanten vom Überhang zum 2. Turm
        self.kanten.append(kante(neue_ecken[-1], self.ecken[-2], self.stat, self.dyn))
        self.kanten.append(kante(neue_ecken[-1], self.ecken[-4], self.stat, self.dyn))
        self.kanten.append(kante(neue_ecken[-2], self.ecken[-4], self.stat, self.dyn))
        
        self.ecken.extend(neue_ecken)
        
        #self.kanten[self.höhe_turm*4 + 1].delete()
        #self.kanten[self.höhe_turm*4 + 1] = None
        

    
    def run(self):
        durchläufe = 300
        n = 200
        t = time.time()
        for i in range(100):
            self.dyn.durchlaufe_events(0.001, fe_support=0)
        self.dyn.rev_kanten_stat()
        self.stat.berechne()
        for i in range(200):
            self.dyn.durchlaufe_events(0.001, fe_support=1)
        while len(self.dyn.ecken_update) > 0:
            for i in range(100):
                self.dyn.durchlaufe_events(0.001, fe_support=0)
            durchläufe += 100  
        print("Zeit: ")
        print(time.time() - t)
        
        self.mplot.cla()
            
        for obj in [self.ecken, self.st_ecken, self.kanten]:
            self.mplot.add(obj)
            
        self.mplot.draw(intervall=0.01)
        print("Durchläufe: ")
        print(durchläufe)
        
    
    def run2(self):
        durchläufe = 0
        self.stat.berechne()
        erg = np.array([k.res_kraft for k in self.kanten])
        old = np.array([k.reale_kraft for k in self.kanten])
        changes = list()
        konv = list()
        while len(self.dyn.ecken_update) > 0:
            for i in range(30):
                self.dyn.durchlaufe_events(0.001, fe_support=0)
                new = np.array([k.reale_kraft for k in self.kanten])
                changes.append(sum(abs(old - new)))
                konv.append(sum(abs(erg - new)))
                old = new
            durchläufe += 30
        
            self.mplot.cla()
            
            for obj in [self.ecken, self.st_ecken, self.kanten]:
                self.mplot.add(obj)
            
            self.mplot.draw(intervall=0.01)
        print("Durchläufe: ")
        print(durchläufe)
        plt.figure()
        plt.title("Delta")
        plt.plot(changes)
        plt.figure()
        plt.title("Konvergenz")
        plt.plot(konv)
        plt.show()