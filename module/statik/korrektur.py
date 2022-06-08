
""" Die geniale Erfindung der Korrektur. """

class korrektur:
	pass
    
    
    
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