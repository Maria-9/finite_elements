
""" Ein Statik Objekt führt Listen von Pointern auf alle zur Berechnung der Statik notwendigen Werte. Mittels einer Berechnungsfunktion lässt sich dann die aktuelle
    Kräfteverteilung berechnen.
"""
import numpy as np
from scipy.sparse.linalg import lsqr
from messagebox import msg
from .nummeriert import nummeriert
from .row_limited_csc import row_limited_csc
from .dynamische_ecke import dynamische_ecke
from .statische_ecke import statische_ecke
from .kante import kante

class statik:

    """ 
    Beschreibung:
        Ein Statik Objekt führt Listen für alle zur Berechnung der Statik notwendigen Werte. Mittels einer Berechnungsfunktion lässt sich dann die aktuelle
        Kräfteverteilung berechnen.
    
    
    Öffentliche Methoden:
        inkludiere(obj : nummeriert)    -> Fügt Zeiger die wirkenden Kräfte von obj. hinzu.
        exkludiere(obj : nummeriert)    -> Entfernt alle Daten/Referenzen im Statik-Objekt, die mit dem Objekt verbunden sind.
        berechne()                      -> Berechnet die resultierende Kräfteverteilung, gegeben den ansetzenden Kräften.
    """
    
    def __init__(self, num_ecken, num_kanten, dynamik, dim = 2):
        self.dim = dim                                  # die Dimension in der sich die Statik bewegt.
        self.ecken_ans = np.zeros(num_ecken*self.dim)   # die an den Eckpunkten ansetzenden Kräfte e_a
        self.ecken_res = np.zeros(num_ecken*self.dim)   # die an den Eckpunkten resultierenden Kräfte nach der berechnung e_r = e_a + S * k_r
        self.kanten_res = np.zeros(num_kanten)          # die an den Kanten resultierenden Kräfte k_r = S^(-1) * e_a
        self.struktur_matrix = row_limited_csc.empty(2*self.dim, len(self.kanten_res), dtype=float)      # die Strukturmatrix.
        
        #self.dyn = dynamik
        #self.ecken_bewege = dict()   # wenn es Kräfte gibt, die auf eine Ecke wirken, so passt diese mit ihrer Bewege - Methode ihren Zustand an.
  
    def inkludiere(self, obj : nummeriert):
        """ Setzt alle Parameter im Statik-Objekt um das Objekt 'obj' in Zukunft in die Berechnung der Statik mit einzubinden."""
        
        # obj == Ecke
        if obj.nummeriert_als(dynamische_ecke):
            # stelle sicher, dass es Plätze für die Kräfte der Ecke gibt.
            if len(self.ecken_ans) <= obj.nummer*self.dim:
                supplement = np.zeros((self.dim*(obj.nummer+1) - len(self.ecken_ans),))
                self.ecken_ans = np.concatenate((self.ecken_ans, supplement))
                self.ecken_res = np.concatenate((self.ecken_res, supplement))
            else:
                for array in [self.ecken_ans, self.ecken_res]:
                    if (np.array(array[obj.nummer*self.dim : (obj.nummer+1)*self.dim]) != [0]*self.dim).any():
                        msg.warning("Der Speicherplatz auf den die neue Ecke zugreift war ungleich 0.")
            
            # füge die Bewege- Methode der Ecke hinzu.
            #if obj.nummer in self.ecken_bewege:
            #    msg.warning("Die Bewege- Methode einer Ecke wurde unerwartet durch eine andere Bewegungs- Methode eier anderen ersetzt.")
            #self.ecken_bewege[obj.nummer] = obj.bewege
        
        # obj == Kante
        if obj.nummeriert_als(kante):
            
            # berechne die Kräfteverteilung auf die Ecken - bzw. die relative Verteilung
            # (- also die zur Kante gehörige Spalte in der Strukturmatrix.)
            
            vec = [list(), list()] # indizes, daten
            for e in [obj.ecke1, obj.ecke2]:
                if e.__class__ != statische_ecke:
                    vec[0].extend([e.nummer * self.dim + i for i in range(self.dim)])
                    vec[1].extend(e.richtung_von(obj.gib_nachbar(e)))

            # Bringe die Daten direkt in das korrekte Format.
            (bf_ind, bf_data) = self.struktur_matrix._backfilling(vec[0])
            vec[0] += bf_ind
            vec[1] += bf_data
            
            if np.shape(vec) != (2, 2 * self.dim):
                raise Exception("Weird things happened")
            
            if len(self.kanten_res) != len(self.struktur_matrix.indptr) - 1:
                raise Exception("Es gibt nicht gleich viele Einträge in 'kanten_res', als es Spalten in der Strukturmatrix gibt.")
                # Im Folgenden wird angenommen, dass die Länge von kanten_res immer gleich der Anzahl an Spalten in der Strukturmatrix ist.
     
     
            if len(self.kanten_res) <= obj.nummer:
            
                # erweitere die Plätze für die Kantenkräfte
                supplement = np.zeros((obj.nummer - len(self.kanten_res) + 1,))
                self.kanten_res = np.concatenate((self.kanten_res, supplement))
                
                # erweitere die Strukturmatrix
                #   erzeuge leere Matrix der richtigen Form
                indptr = [i*2*self.dim for i in range(len(supplement) + 1)]
                indices = [i for i in range(2*self.dim)] * (len(supplement))
                data = [0] * len(indices)
                #   schreibe die Kräfteverteilung hinein
                indices[len(indices)-2*self.dim : len(indices)] = vec[0]
                data[len(indices)-2*self.dim : len(indices)] = vec[1]
                
                #   hänge die Matrix an die Strukturmatrix an.
                self.struktur_matrix.append((data, indices, indptr), fast=True)

            else:
                # Ich kann leider nicht sagen, wie sinnvoll es ist diese Warnung nicht zu werfen. Werfen wir sie nicht, ist die inkludiere-Funktion 
                # vielseitiger einsetzbar.
                #if self.kanten_res[obj.nummer] != 0:
                #    msg.warning("Der Speicherplatz auf den die neue Kante zugreift war ungleich 0.")
                
                # trage die Kräfteverteilung in die Strukturmatrix ein.
                self.struktur_matrix.override((vec[1], vec[0]), obj.nummer)
        
    def exkludiere(self, obj : nummeriert):
        """ Gibt alle Plätze in den Arrays und in der Strukturmatrix frei, damit diese neu verwendet werden können. """
        # obj == Ecke
        if obj.nummeriert_als(dynamische_ecke):
            i = [obj.nummer * self.dim + i for i in range(self.dim)]
            self.ecken_ans[i] = [0] * self.dim  
            self.ecken_res[i] = [0] * self.dim
            
            #if self.ecken_bewege.pop(obj.nummer, None) == None:
            #    msg.warning("Es wurde eine Ecke exkluiert, von der keine Beweges-Methode bekannt war.")

        # obj == Kante
        if obj.nummeriert_als(kante):
            self.kanten_res[obj.nummer] = 0
            self.struktur_matrix.override(([0]*2*self.dim, [i for i in range(2*self.dim)]), obj.nummer) # Diese Zeile ist sehr wichtig.

    def revidiere(self, obj : nummeriert):
        """ verändere die Einträge in der Strukturmatrix, die die Richtungen zu den Ecken einer Kante angeben. """
        if obj.nummeriert_als(kante):
            if len(self.kanten_res) <= obj.nummer:
                raise Exception("Revidierung der Kante innerhalb der Statik ist fehlgeschlagen")
            self.inkludiere(obj)
    
    def berechne(self):
        """ Funktionsweise:
        a := ecken_ans
        e := ecken_res
        S := struktur_matrix
        r := kanten_res
        
        Es gibt eine neue ansetzende Kraft a.
        Minimiere über r die Norm von
          e = Sr + a = S*dr + (a + S*r_0)
        Dies entspricht dem Lösen des least-squares Problem von S*dr = -a - S*r_0
            mit r = dr + r_0, wobei r_0 die alte resultierende Kraft ist.
        """
        # Die Rechengeschwindigkeit kann ev. verbessert werden, indem (- self.ecken_ans - self.struktur_matrix.dot(self.kanten_res))
        # in ein ss.bsr_array gecaset wird. (Ist hierfür eine neue Version von scipy notwendig?)
        # Des weiteren könnte der lsrq - Optimierer durch eine eigene Version verschnellert werden, indem eine sparse List of List - Matrix mitgeführt.
        # Über diese könnte für jede Knotenkraft, die sich verändert hat, die Kanten ermittelt werden, über die eine Optimierung notwendig ist.
        
        erg = lsqr(self.struktur_matrix, - self.ecken_ans - self.struktur_matrix.dot(self.kanten_res),
                       damp = 0, atol = 0.00001, btol = 0.00001, iter_lim = 1000, show = False)
        dr = erg[0]
        self.kanten_res = dr + self.kanten_res
        self.ecken_res = self.struktur_matrix.dot(self.kanten_res) + self.ecken_ans 
            # ecken_res wird in der Update Methode nicht verwendet
        
        #msg.info("Statik Berechnung:\n" +
        #           " Gestoppt bei Iteration: " + str(erg[2]) + "\n" +
        #           " 1-Norm der Abweichung: " + str(erg[3]))
        
        #msg.info("Anzahl der Kanten mit veränderten resultierenden Kräften: " + str(sum((dr >= 0.05) + (dr <= -0.05))))

        #for i, v in enumerate(abs(self.ecken_res) >= 0.001):
        #    if v == True:
        #        self.dyn.ecken_bewege.add(self.ecken_bewege[i // self.dim])
            