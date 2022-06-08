
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
        [Nicht mehr aktuell]
        inkludiere(obj : nummeriert)    -> Fügt Zeiger die wirkenden Kräfte von obj. hinzu.
        exkludiere(obj : nummeriert)    -> Entfernt alle Daten/Referenzen im Statik-Objekt, die mit dem Objekt verbunden sind.
        berechne()                      -> Berechnet die resultierende Kräfteverteilung, gegeben den ansetzenden Kräften.
    """
    
    def __init__(self, sphäre, num_kanten):
        self.dim = sphäre.dim                     # die Dimension in der sich die Statik bewegt.
        
        self.sphäre = sphäre
            # Es wird zugegriffen auf:
            # sphäre.ecken_ans                         # die an den Eckpunkten ansetzenden Kräfte e_a
            # sphäre.ecken_res                         # die an den Eckpunkten resultierenden Kräfte nach der berechnung e_r = e_a + S * k_r
            # sphäre.kanten_res                        # die an den Kanten resultierenden Kräfte k_r = S^(-1) * e_a
        
                  
        self.struktur_matrix = row_limited_csc.empty(2*self.dim, num_kanten, dtype=float)      # die Strukturmatrix S.
  
    def inkludiere_kante(self, kante):
        """ Setzt alle Parameter im Statik-Objekt um die Kante 'kante' in Zukunft in die Berechnung der Statik mit einzubinden."""
        
        # berechne die Kräfteverteilung auf die Ecken - bzw. die relative Verteilung
        # (- also die zur Kante gehörige Spalte in der Strukturmatrix.)
        
        vec = [list(), list()] # indizes, daten
        for e in [kante.ecke1, kante.ecke2]:
            if e.__class__ != statische_ecke:
                vec[0].extend([e.nummer * self.dim + i for i in range(self.dim)])
                vec[1].extend(e.richtung_von(kante.gib_nachbar(e)))

        # Bringe die Daten direkt in das korrekte Format.
        (bf_ind, bf_data) = self.struktur_matrix._backfilling(vec[0])
        vec[0] += bf_ind
        vec[1] += bf_data
        
        if np.shape(vec) != (2, 2 * self.dim):
            raise Exception("Weird things happened")
 
        if len(self.struktur_matrix.indptr) - 1 <= kante.nummer:
        
            # erweitere die Strukturmatrix
            #   erzeuge leere Matrix der richtigen Form
            indptr = [i*2*self.dim for i in range(kante.nummer - len(self.struktur_matrix.indptr) + 3)]
            indices = [i for i in range(2*self.dim)] * (kante.nummer - len(self.struktur_matrix.indptr) + 2)
            data = [0] * len(indices)
            #   schreibe die Kräfteverteilung hinein
            indices[len(indices)-2*self.dim : len(indices)] = vec[0]
            data[len(indices)-2*self.dim : len(indices)] = vec[1]
            
            #   hänge die Matrix an die Strukturmatrix an.
            self.struktur_matrix.append((data, indices, indptr), fast=True)

        else:
        
            # trage die Kräfteverteilung in die Strukturmatrix ein.
            self.struktur_matrix.override((vec[1], vec[0]), kante.nummer)
        
        if len(self.sphäre.kanten_res) != len(self.struktur_matrix.indptr) - 1:
            raise msg.error("Es gibt nicht gleich viele Einträge in 'kanten_res', als es Spalten in der Strukturmatrix gibt.")
            # Dies sollte nach der Aufnahme einer Kante stets der fall sein.
 
        
    def exkludiere_kante(self, kante):
        """ Gibt alle Plätze in der Strukturmatrix frei, damit diese neu verwendet werden können. """
        self.struktur_matrix.override(([0]*2*self.dim, [i for i in range(2*self.dim)]), kante.nummer) # Diese Zeile ist sehr wichtig.

    def revidiere(self, kante):
        """ verändere die Einträge in der Strukturmatrix, die die Richtungen zu den Ecken einer Kante angeben. """
        if kante.nummeriert_als(kante):
            if len(self.sphäre.kanten_res) <= kante.nummer:
                raise Exception("Revidierung der Kante innerhalb der Statik ist fehlgeschlagen")
            self.inkludiere_kante(kante)
        else:
            raise Exception("Revidierung eines Objektes innerhalb der Statik ist fehlgeschlagen")
    
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
        # Die Rechengeschwindigkeit kann ev. verbessert werden, indem (- self.sphäre.ecken_ans - self.struktur_matrix.dot(self.sphäre.kanten_res))
        # in ein ss.bsr_array gecaset wird. (Ist hierfür eine neue Version von scipy notwendig?)
        # Des weiteren könnte der lsrq - Optimierer durch eine eigene Version verschnellert werden, indem eine sparse List of List - Matrix mitgeführt.
        # Über diese könnte für jede Knotenkraft, die sich verändert hat, die Kanten ermittelt werden, über die eine Optimierung notwendig ist.
        
        erg = lsqr(self.struktur_matrix, - self.sphäre.ecken_ans - self.struktur_matrix.dot(self.sphäre.kanten_res),
                       damp = 0, atol = 0.00001, btol = 0.00001, iter_lim = 1000, show = False)
        dr = erg[0]
        self.sphäre.kanten_res = dr + self.sphäre.kanten_res
        self.sphäre.ecken_res = self.struktur_matrix.dot(self.sphäre.kanten_res) + self.sphäre.ecken_ans 
        
        #msg.info("Statik Berechnung:\n" +
        #           " Gestoppt bei Iteration: " + str(erg[2]) + "\n" +
        #           " 1-Norm der Abweichung: " + str(erg[3]))
        
        #msg.info("Anzahl der Kanten mit veränderten resultierenden Kräften: " + str(sum((dr >= 0.05) + (dr <= -0.05))))         