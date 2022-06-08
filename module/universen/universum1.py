
from ..statik.sphäre import sphäre
from ..statik.matplot import matplot
from ..statik.plotable_inheritances  import p_dynamische_ecke
from ..statik.plotable_inheritances  import p_statische_ecke
from ..statik.plotable_inheritances  import p_kante
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
        
        self.sphäre = sphäre(num_ecken, num_kanten)
        
        self.st_ecken = list()
        self.ecken = list()
        self.kanten = list()
        
        self.mplot = matplot()
        
        dyn_ecke = lambda position : p_dynamische_ecke(self.sphäre, position)
        stat_ecke = lambda position : p_statische_ecke(self.sphäre, position)
        kante = lambda ecke1, ecke2, darstellung=0 : p_kante(self.sphäre, ecke1, ecke2, darstellung=darstellung)
        
        #baue den Turm
        for i in range(höhe_turm*2):
            if i % 2 == 0:
                e = dyn_ecke((1, i / 2 + 1))
            else:
                e = dyn_ecke((2, (i+1) / 2))
            self.ecken.append(e)
        
        #setze Eckpunkt
        self.ecken.append(dyn_ecke((2, höhe_turm + 1)))
        
        #baue nach rechts
        for i in range(2*länge_überhang):
            if i % 2 == 0:
                e = dyn_ecke((3 + i/2, höhe_turm))
            else:
                e = dyn_ecke((2 + (i+1)/2, höhe_turm + 1))
            self.ecken.append(e)
        
        #baue den Balancierpunkt für eine Wage
        self.ecken.append(dyn_ecke((3 + länge_überhang, höhe_turm+1)))
        self.ecken.append(dyn_ecke((3 + länge_überhang, höhe_turm+2)))
        
        #setze zwei statischen Ecken am Boden
        prev_2 = stat_ecke((1, 0))
        prev_1 = stat_ecke((2, 0))
        
        self.st_ecken.extend([prev_2, prev_1])
        
        #setze die Kanten
        for e in self.ecken:
        
            self.kanten.append(kante(prev_2, e))
            self.kanten.append(kante(prev_1, e))
            
            prev_2 = prev_1
            prev_1 = e
        
        #setze eine doppelte Kante
        self.kanten.append(kante(self.ecken[höhe_turm*2 - 1], self.ecken[höhe_turm*2], darstellung = 1))
        
        # baue die Wage
        self.ecken.append(dyn_ecke((1 + länge_überhang, höhe_turm+3)))
        self.ecken.append(dyn_ecke((5 + länge_überhang, höhe_turm+3)))
        self.ecken.append(dyn_ecke((5 + länge_überhang, höhe_turm+4)))
        
        self.kanten.append(kante(self.ecken[-4], self.ecken[-3]))
        self.kanten.append(kante(self.ecken[-4], self.ecken[-2]))
        self.kanten.append(kante(self.ecken[-2], self.ecken[-3]))
        self.kanten.append(kante(self.ecken[-1], self.ecken[-2]))


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
         
        delta = 0
        zeitschritt = 2
        durchläufe = 0
        t = time.time()
        for j in range(50):
            
            self.sphäre.physik.berechne(delta)
            
            durchläufe += 1
            print(durchläufe)
            
            self.mplot.cla()
            
            for obj in [self.ecken, self.st_ecken, self.kanten]:
                self.mplot.add(obj)
            
            self.mplot.draw(intervall=0.001)
            
            t_neu = time.time()
            delta = t_neu - t
            print("Delta: " + str(delta))
            t = t_neu
            #print("Delta: " + str(delta))
            #print("Time: " + str(time.time() - t))
    
    def run_easy(self):
        self.sphäre.physik.berechne()
        for obj in [self.ecken, self.st_ecken, self.kanten]:
            self.mplot.add(obj)
        self.mplot.draw()
        #self.mplot.show()