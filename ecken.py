
# Elementare Klassen der Finiten Elemente Analyse

# Im folgenden Ordner ist das 'messagebox' Modul gespeichert.
import sys
sys.path.insert(1, 'C:\\Users\\Sebastian Hahn\\AppData\\Roaming\\Notepad++\\plugins\\config\\PythonScript\\npp_environment')

import numpy as np
from messagebox import msg
import scipy.sparse as ss


class nummeriert:

    __freie_nummern = list()
    __höchste_nummer = 0
    _kind = "nummeriertes_objekt"   # überschreibe dies
    # Es ist denkbar, statt _kind auch einfach den Klassennamen self.__class__.__name__ zu verwenden.
    
    @classmethod
    def _neue_nummer(cls):
        if len(cls.__freie_nummern) == 0:
            cls.__höchste_nummer += 1
            return cls.__höchste_nummer - 1
        else:
            return cls.__freie_nummern.pop()
    
    def __init__(self):
        self.nummer = self.__class__._neue_nummer()
        msg.info(str(self.__class__))
        
    def __del__(self):
        self.__class__.__freie_nummern.append(self.nummer)
    
    def __str__(self):
        return "\n Nummer: " + str(self.nummer) + "\t[" + self.__class__._kind + "]"
    

class ecke(nummeriert):

    # __slots__ = ['nummer', 'dynamisch', 'position', 'ansetzende_kraft', 'resultierende_kraft', 'masse', kanten', 'nachbarn']
    _kind = "Ecke"
    
    def __init__(self, position):
        self.position = position
        self.kanten = list()
        self.nachbarn = list()
        
        super().__init__()
    
    def __del__(self):
        super().__del__()
    
    def neue_kante(self, kante):
        nachbar = kante.gib_nachbar(self)

        if nachbar in self.nachbarn:
            msg.error("Es gibt bereits eine Kante zwischen " + str(self.nummer) + " und " + str(nachbar.nummer))
            raise ValueError("Es gibt bereits eine Kante zwischen " + str(self.nummer) + " und " + str(nachbar.nummer))
        
        if kante in self.kanten:
            msg.error("Die Kante " + str(kante) + " ist bereits in der Liste der Kanten der Ecke " + self.nummer + " vorhanden.")
            raise ValueError("Die Kante " + str(kante) + " ist bereits in der Liste der Kanten der Ecke " + self.nummer + " vorhanden.")
        
        self.nachbarn.append(nachbar)
        self.kanten.append(kante)
    
    def entferne_kante(self, kante):
        nachbar = kante.gib_nachbar(self)
        if self.nachbarn.index(nachbar) != self.kanten.index(kante):
            raise IndexError("Der erste Index des Nachbarn stimmt nicht mit dem Ersten Index der Kante überein.")
        self.nachbarn.remove(nachbar)
        self.kanten.remove(kante)
            
    
    
    def aktualisiere_strukturmatrix():
        print("noch nicht implementiert")
    
    def __str__(self):
        return ("----------------------------"
                + super().__str__() # dies ist die Nummerierung
                + "\n Position: " + str(self.position)
                + "\n Kanten : " + str([k.nummer for k in self.kanten])
                + "\n Nachbarn : " + str([n.nummer for n in self.nachbarn]))


class dynamische_ecke(ecke):
    
    _kind = "dynamisch"
    
    def __init__(self, position, masse):
        self.masse = masse
        self.ansetzende_kraft = 0
        self.resultierende_kraft = 0
        super().__init__(position)
        
    
    def __str__(self):
        return (super().__str__()
                + "\n Masse : " + str(self.masse)
                + "\n Ansetzende Kraft: " + str(self.ansetzende_kraft)
                + "\n Resultierende Kraft: " + str(self.resultierende_kraft))
    

class statische_ecke(ecke):
    
    _kind = "statisch"
    
    def __init__(self, position):
        super().__init__(position)


class kante(nummeriert):

    _kind = "Kante"
    
    def __init__(self, ecke1, ecke2):
        self.ecke1 = ecke1
        self.ecke2 = ecke2
        
        ecke1.neue_kante(self)
        ecke2.neue_kante(self)
        
        self.resustierende_kraft = 0
        
        super().__init__()
    
    def gib_nachbar(self, ecke):
        if ecke is self.ecke1:
            return self.ecke2
        if ecke is self.ecke2:
            return self.ecke1
        msg.error("Die Ecke ist kein Endpunkt der Kante")
        return None
    
    def auflösen(self):
        self.ecke1.entferne_kante(self)
        self.ecke2.entferne_kante(self)
        
    def __del__(self):
        super().__del__()
    
    def __str__(self):
        return (super().__str__()
                + "\n Ecken: [" + str(self.ecke1.nummer) + ", " + str(self.ecke2.nummer) + "]")
                

class statik:
    
    def __init__(self, dim = 2, ecken_ans = np.array(0), ecken_res = np.array(0), kanten_res = np.array(0)):
        self.dim = dim                          # die Dimension in der sich die Statik bewegt.
        self.ecken_ans = ecken_ans              # die an den Eckpunkten ansetzenden Kräfte e_a
        self.ecken_res = ecken_res              # die an den Eckpunkten resultierenden Kräfte nach der berechnung e_r = e_a + S * k_r
        self.kanten_res = kanten_res            # die an den Kanten resultierenden Kräfte k_r = S^(-1) * e_a
        self.struktur_matrix = ss.csc_matrix((dim * 2, length(kanten_ans)))      # die Strukturmatrix - für jede Kante gibt es dim * 2 Einträge für die Ecken.
        
    def neue_kante(self, kante):
        pass
        
    def aktualisiere_kante(self, kante):
        pass
    
    def entferne_kante(self, kante):
        pass
    
    def setze_ans_kraft(self, ecke):
        pass
    
    def gib_res_kraft(self, object_mit_res_kraft):
        pass
    
    
    
    
    
if __name__ == "__main__":
    msg.state("Start")
    stat = statik()
    print(stat.ecken_ans)
    print(stat.ecken_res)
    print(stat.kanten_res)
    print(stat.struktur_matrix.toarray())
    
    
    
    # c = dynamische_ecke(tuple([2, 2]), 4)
    # print(c)
    # e = dynamische_ecke(tuple([2, 3]), 4)
    # print(e)
    # d = dynamische_ecke(tuple([2, 4]), 4)
    # print(d)
    # k = kante(c, d)
    # l = kante(e, d)
    # print(l)
    # l.auflösen()
    # l = kante(c, e)
    # print(k)
    # print(l)
    # print(l.ecke2)
    
    
    
    
    