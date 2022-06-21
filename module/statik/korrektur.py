
""" Die geniale Erfindung der Korrektur. """

import scipy.sparse as ss

class korrektur:
    
    """
    Wir lösen das Minimierungsproblem
            sum_{i<j} { (e_i - e_j)^T (e_i - e_j) - p_ij }^2
    wobei p_ij die gewünschte Länge der Kanten ist.
    
    Ich gehe davon aus, dass während der Simulation keine statischen Ecken hinzukommen.
    Dann lassen sich die statischen Ecken in der Strukturmatrix links neben die dynamischen Ecken schreiben, ohne dass die Sortierung verloren geht.
    """
    def __init__(self, sphäre, num_kanten, num_stat_ecken, num_dyn_ecken):
        self.sphäre = sphäre
        
        self.num_stat_ecken = num_stat_ecken
        
        self.strukturmatrix = ss.dok_matrix((num_kanten, num_stat_ecken + num_dyn_ecken))

    def index(self, ecke):
        if ecke.nummeriert_als(statische_ecke):
            return ecke.nummer
        return ecke.nummer + self.num_stat_ecken
   
    def übernehme(self, kante):
    
        # Schritt 1: passe die Shape der Matrix an.
        # (Ich verstehe nicht ganz, weshalb scipy so ein Bums aus der korrekten Shape macht, das zieht nur unnötig viel Code mit sich)
    
        (zeilen, spalten) = self.strukturmatrix.get_shape()
        
        for ecke in [kante.ecke1, kante.ecke2]:
            
            # Man bedenke, dass niemals beide Ecken statische Ecken sein sollten.
            if kante.ecke.nummeriert_als(statische_ecke) and ecke.nummer >= self.num_stat_ecken:
                # Vorsicht! Hier wirds ineffizient
                self.erweitere_strukturmatrix_stat_ecke(ecke)
            
            if kante.ecke.nummeriert_als(dynamische_ecke) and ecke.nummer + self.num_stat_ecken >= spalten
                spalten = ecke.nummer + self.num_stat_ecken + 1
        
        if kante.nummer >= zeilen:
            zeilen = kante.nummer + 1
        
        if (zeilen, spalten) != self.strukturmatrix.get_shape():
            self.strukturmatrix.resize(zeilen, spalten)
            
        # Schritt 2: Übernehme die Kante in die Matrix
        self.strukturmatrix[kante.nummer, self.index(kante.ecke1)] = 1
        self.strukturmatrix[kante.nummer, self.index(kante.ecke2)] = -1
    
    
    def erweitere_strukturmatrix_stat_ecke(self, ecke):
        diff = - self.num_stat_ecken + ecke.nummer + 1
        
        (zeilen, spalten) = self.strukturmatrix.get_shape()
        strukturmatrix = ss.dok_matrix((zeilen, spalten + diff))
        
        for (i, j) in self.strukturmatrix.keys():
            if j < self.num_stat_ecken:     # es handelt sich um die Spalte einer statischen Ecke
                strukturmatrix[i, j] = self.strukturmatrix[i, j]
            else:                           # es handelt sich um die Spalte einer dynamischen Ecke
                strukturmatrix[i, j + diff] = self.strukturmatrix[i, j]
                
    
        self.num_stat_ecken = ecke.nummer + 1
        self.strukturmatrix = strukturmatrix
        
    def korrigiere(self):
        berechne_gewünschte_länge()
        
    
    def berechne_gewünschte_länge(self):
        self.längen = self.sphäre.natürliche_länge / ((self.sphäre.kanten_res**2 / (self.sphäre.elastizitätsmodul + self.sphäre.natürliche_länge)) + 1)
    
    def objective(self):
        
        # berechne die Differenzen
        l = len(self.sphäre.stat_ecken_pos) + len(self.sphäre.ecken_pos)
        pos = np.concatenate((self.sphäre.stat_ecken_pos, self.sphäre.ecken_pos)).reshape((l / 3, 3))
        diff = self.strukturmatrix.dot(pos)         # Matrixprodukt
        diff = diff.multiply(diff)                  # Punktweise Multiplikation
        diff.sum(1)                                 # Summe über die Zeilen
        d = diff - self.längen * self.längen        # Differenz der Quadrate der tatsächlichen und gewünschten Längen
        obj = (d*d).sum()                           # Bilde Least Squares
        
        return obj
        
        
        
        
    
    
    
"""
NOTIZEN AUS DEM KANTEN-MODUL
----------------------------

def kraft_zu_länge(self, kraft):
        ''' Umkehrfunktion zu 'berechne_reale_kraft' '''
        return (self.natürliche_länge / (1 + kraft / self.elastizitätsmodul))^2
    
    def berechne_reale_kraft(self, dynamik, tol = 1):
        # Die Toleranz 'tol' gibt an, ab wann die Differenz zwischen der realen Kraft und
        # der aus der aktuellen Stauchung der Kante entstehenden Kraft klein genug ist, damit die reale Kraft nicht angepasst wird.
        # Hierzu wird diese Toleranz erst durch den Elastizitätsmodul und die natürliche Länge der Kante geteilt.
        
        aktuelle_länge = np.linalg.norm(self.ecke1.position - self.ecke2.position)
        
        # Im wesentlichen ist eine Differentialgleichung gegeben:
        #   l'(f) = (f * l(f)^2) / (V * E)  , wobei
        #   l(f) Die Länge des Stabes bei einwirkender Kraft f ist
        #   V das Volumen des Stabes, und
        #   E das Elastizitätsmodul
        #
        # Wofram Alpha schlägt als Lösung f = sqrt( 2*E*V*(1 - L/l) ) vor, dies entspricht in etwa der Wurzel des obigen antiproportionalen Verhältnisses.
        # Nehmen wir an, dass das Volumen eines Stabes proportional zu seiner Länge zunimmt ergeben sich die folgenden Gleichungen.
        # Es ist denkbar die Wurzel zu Vernachlässigen, um bessere Performance zu erzielen.
        
        antiprop = self.elastizitätsmodul * self.natürliche_länge * (self.natürliche_länge / aktuelle_länge - 1)

        neue_reale_kraft = math.sqrt(antiprop)
        
        ''' Dies wird lediglich für Bewegungen benötigt.
        
        if abs(self.__reale_kraft - neue_reale_kraft) > tol / (self.elastizitätsmodul * self.natürliche_länge):
            self.__reale_kraft = neue_reale_kraft
            dynamik.kanten_rev.add(self.revidiere_statik)
            dynamik.ecken_update.add(self.ecke1.update)
            dynamik.ecken_update.add(self.ecke2.update)
        '''
        
        return self.__reale_kraft
    
    def revidiere_statik(self):
        self.setze_res_kraft = self.__reale_kraft
        self.statik.revidiere(self)
   
   
NOTIZEN AUS DEM DYNAMIK-MODUL
-----------------------------

    def rev_kanten_stat(self):
        ''' Revidiere die Einträge in der Statik, die alle veränderten Kanten betreffen.'''
        while(len(self.kanten_rev) > 0):
            self.kanten_rev.pop()()
--------------------------------------------
"""