
from ..statik.dynamik import dynamik
from ..statik.statik import statik
from ..statik.matplot import matplot
from ..statik.plotable_inheritances  import p_dynamische_ecke as dynamische_ecke
from ..statik.plotable_inheritances  import p_statische_ecke as statische_ecke
from ..statik.plotable_inheritances  import p_kante as kante
#from ..statik.dynamische_ecke import dynamische_ecke
#from ..statik.statische_ecke import statische_ecke
#from ..statik.kante import kante
import messagebox as msg
import numpy as np
from matplotlib import pyplot as plt
import time

    
class universum1:
    
    def __init__(self):
        höhe_turm = 5
        länge_überhang = 2
        num_ecken = 2*(höhe_turm + länge_überhang) + 1
        num_kanten = 2 * num_ecken 
        self.dyn = dynamik()
        #self.stat = statik(num_ecken, num_kanten) # Je genauer die Werte für num sind, desto weniger Rechenzeit wird zum Aufbau benötigt.
        self.stat = statik(1, 1, self.dyn)
        self.st_ecken = list()
        self.ecken = list()
        self.kanten = list()
        self.mplot = matplot()
        
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
        
        #baue den Balancierpunkt für eine Wage
        self.ecken.append(dynamische_ecke((3 + länge_überhang, höhe_turm+1), self.stat, self.dyn))
        self.ecken.append(dynamische_ecke((3 + länge_überhang, höhe_turm+2), self.stat, self.dyn))
        
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
        
        #setze eine doppelte Kante
        self.kanten.append(kante(self.ecken[höhe_turm*2 - 1], self.ecken[höhe_turm*2], self.stat, self.dyn, darstellung = 1))
        
        # baue die Wage
        self.ecken.append(dynamische_ecke((1 + länge_überhang, höhe_turm+3), self.stat, self.dyn))
        self.ecken.append(dynamische_ecke((5 + länge_überhang, höhe_turm+3), self.stat, self.dyn))
        self.ecken.append(dynamische_ecke((5 + länge_überhang, höhe_turm+4), self.stat, self.dyn))
        
        self.kanten.append(kante(self.ecken[-4], self.ecken[-3], self.stat, self.dyn))
        self.kanten.append(kante(self.ecken[-4], self.ecken[-2], self.stat, self.dyn))
        self.kanten.append(kante(self.ecken[-2], self.ecken[-3], self.stat, self.dyn))
        self.kanten.append(kante(self.ecken[-1], self.ecken[-2], self.stat, self.dyn))

    
    def run2(self):
        durchläufe = 0
        self.stat.berechne()
        erg = np.array([k.res_kraft for k in self.kanten])
        old = np.array([k.reale_kraft for k in self.kanten])
        changes = list()
        konv = list()
        while len(self.dyn.ecken_update) > 4:
            print(len(self.dyn.ecken_update))
            for i in range(1000):
                self.dyn.durchlaufe_events(0.001, fe_support=0)
                new = np.array([k.reale_kraft for k in self.kanten])
                changes.append(sum(abs(old - new)))
                konv.append(sum(abs(erg - new)))
                old = new
            durchläufe += 1000
        
            self.mplot.cla()
            
            for obj in [self.ecken, self.st_ecken, self.kanten]:
                self.mplot.add(obj)
            
            self.mplot.draw(intervall=1)
        print("Durchläufe: ")
        print(durchläufe)
        plt.figure()
        plt.title("Delta")
        plt.plot(changes)
        plt.figure()
        plt.title("Konvergenz")
        plt.plot(konv)
        plt.show()
    
    def run(self):
    
        for k in range(1000):
            self.dyn.durchlaufe_events(0.001, fe_support=0)
        delta = 0
        zeitschritt = 2
        for j in range(1000):
            t = time.time()
            durchläufe = 0
            t_b = t
            while(time.time() - t - zeitschritt + delta < 0):
                for i in range(10):
                    self.dyn.durchlaufe_events(0.001, fe_support=0)
                durchläufe += 10
            t_a = time.time()
            #print("Zeitschritt: " + str(time.time() - t_b))
            self.dyn.rev_kanten_stat()
            self.stat.berechne()
            self.dyn.bewege_ecken(0.02)
            print(durchläufe)
            self.mplot.cla()
            
            for obj in [self.ecken, self.st_ecken, self.kanten]:
                self.mplot.add(obj)
            
            self.mplot.draw(intervall=0.00001)
            
            delta = time.time() - t_a
            #print("Delta: " + str(delta))
            #print("Time: " + str(time.time() - t))