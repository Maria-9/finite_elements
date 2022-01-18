
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
    
    def __init__(self, position, masse, statik=None):
        #TODO: dynamische ecken tragen sich in der statik ein.
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
    # statische Ecken tragen sich nicht in der statik ein.
    # statische Ecken dienen lediglich als Fixpunkte.
    _kind = "statisch"
    
    def __init__(self, position):
        super().__init__(position)


class kante(nummeriert):

    _kind = "Kante"
    
    def __init__(self, ecke1, ecke2, statik=None):
        # TODO: die Kante trägt sich in der statik ein.
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
    
    def __init__(self, dim = 2, ecken_ans = np.array([0]), ecken_res = np.array([0]), kanten_res = np.array([0])):
        self.dim = dim                          # die Dimension in der sich die Statik bewegt.
        self.ecken_ans = ecken_ans              # die an den Eckpunkten ansetzenden Kräfte e_a
        self.ecken_res = ecken_res              # die an den Eckpunkten resultierenden Kräfte nach der berechnung e_r = e_a + S * k_r
        self.kanten_res = kanten_res            # die an den Kanten resultierenden Kräfte k_r = S^(-1) * e_a
        self.struktur_matrix = row_limited_csc(([0], [0], [0,1]), num_rows=2*dim, dtype=float)      # die Strukturmatrix.
        
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
    

    
class row_limited_csc(ss.csc_matrix):
    
    def __init__(self, arg1, num_rows=None, shape=None, dtype=None, copy=False):
        
        # das Argument shape wird benötigt, da ein Konstruktor für eine csc_matrix stets diesen Parameter nimmt. Würde er fehlen, könnte scipy nicht regelkonform
        # mit dieser Klasse rechnen können. Der Parameter erfüllt hier jedoch keinen weiteren Sinn.
        
        # @docstring:
        # Die angegebene Matrix wird vergrößert, falls sie weniger Zeilen enthält als angegeben.
        # Sie wird niemals verkleinert.
          
        ss.csc_matrix.__init__(self, arg1, dtype=dtype, shape=shape, copy=copy)
        
        # Find the maximum number of entries per column and store it in self.num_rows
        self.num_rows = 0
        prev_ptr = 0
        for ptr in self.indptr:
            self.num_rows = max(self.num_rows, ptr - prev_ptr)
            prev_ptr = ptr
        
        # Check the number of allowed rows: num_rows
        if num_rows != None:
            if self.num_rows > num_rows:
                msg.error("In der CSC-Matrix sind mehr Einträge pro Spalte (" + self.num_rows + ") enthalten, als num_rows = " + str(num_rows) + " erlaubt.")
            else:
                self.num_rows = num_rows
        
        if self.num_rows == 0:
            self.num_rows = 1
            msg.error("Es wurde eine row_limited_csc Matrix ohne Zeilen erstellt. Die Zeilenanzahl wurde auf 1 erhöht.")
        
        # correct the format of the matrix.
        
        new_data = []
        new_indices = []
        new_indptr = []
        
        prev_ptr = 0
        for ptr in self.indptr:
            if ptr == 0:
                new_indptr.append(0)
                continue
            
            # Füge die bestehenden Daten ein
            new_data.extend(self.data[prev_ptr : ptr])
            new_indices.extend(self.indices[prev_ptr : ptr])
            
            # Fülle die entstehenden Leerstellen von oben mit Nullen auf, bis es num_row Einträge gibt.
            ind, data = self._backfilling(self.indices[prev_ptr : ptr])
            new_data.extend(data)
            new_indices.extend(ind)
            
            # Check this for debugging reasons:
            if new_indptr[-1] + self.num_rows < ptr:
                raise Exception("Some weird things happened here")
            
            # setze den Pointer
            new_indptr.append(new_indptr[-1] + self.num_rows)
            
            prev_ptr = ptr
            
        
        self.data = np.array(new_data)
        self.indices = np.array(new_indices)
        self.indptr = np.array(new_indptr)
        self._shape = (self.indices.max() + 1, len(new_indptr) - 1)
        
        # setze full_check=False um Zeit zu sparen (O(1) statt O(n))
        self.check_format(full_check=True)
        self.check_doubled_indices()
        
    
    def check_doubled_indices(self):
        prev_ptr = 0
        col = -1
        for ptr in self.indptr:
            
            for i in range(prev_ptr, ptr):
                if (self.indices[i+1: ptr] == self.indices[i]).any():
                    msg.warning("Der Index " + str(self.indices[i]) + " wurde mehrmals in der Spalte " + str(col) + " gefunden.")

            prev_ptr = ptr
            col += 1
    
    def _backfilling(self, present_ind):
    
        # Es sollen 'amount' viele Indizes von Null ab aufgefüllt werden, jedoch nicht die aus present_ind doppelt vorkommen.
        amount = self.num_rows - len(present_ind)
        i = 0
        new_ind = []
        while len(new_ind) < amount:
            if i not in present_ind:
                new_ind.append(i)
            i += 1
        return (new_ind, [0 for i in range(amount)])
        
        # Sofern alle fehlenden Daten mit 0 gefüllt werden, können auch alle fehlenden Indizes mit 0 gefüllt werden.
        # Es kommen dann zwar doppelte Indizes vor, dafür spart man sich jedoch obige Schleife.

    def append(self, triple, fast=False):
        # Vorsicht! Ist fast=True müssen die Eingabedaten bereits in der richtigen Form einer row_limited_csc sein.
    
        if fast:
            # Dies ist das Tripel triple
            (data, indices, indptr) = triple
            
            # Setze die Matrix:
            self.data = np.concatenate([self.data, data])
            self.indices = np.concatenate([self.indices, indices])
            self.indptr = np.concatenate([self.indptr, indptr[1:] + self.indptr[-1]])
            
            # Setze die Korrekte Form
            maximum = max(indices)
            if maximum >= self.shape[0]:
                self._shape = (maximum + 1, self.shape[1] + len(indptr) - 1)
            else:
                self._shape = (self.shape[0], self.shape[1] + len(indptr) - 1)

            # Prüfe Korrektheit im Falle des Debuggens:
            self.check_format(full_check=False)
            
        else:
            csc = row_limited_csc(triple, num_rows=self.num_rows)
            csc = ss.hstack([self, csc])
            self._set_self(csc)

    def append_csc(self, csc_matrix, fast=False):
        # Use this for row_limited_csc matrices.
        
        if not fast:
            self._set_self(ss.hstack([self, row_limited_csc(csc_matrix, num_rows=self.num_rows)]))
        else:
            self.append((csc_matrix.data, csc_matrix.indices, csc_matrix.indptr), fast=True)
    
    def __time_append():
        
        # Das Ergebnis dieses Skriptes besagt, stets die schnellen Varianten zu verwenden. 
        # Für genauere Untersuchungen scheint die time-Methode nicht brauchbar. Evtl. könnte man dies umschreiben auf timeit?
        #
        
        mat = ([1, 2, 3, 4, 5, 6, 7, 8, 9],[0, 2, 4, 0, 2, 1, 3, 5, 4],[0, 1, 1, 2, 8, 9])
        vec = ([7, 7, 7, 9, 8, 9], [0, 1, 2, 3, 4, 5], [0, 6])
        npvec = (np.array(vec[0]), np.array(vec[1]), np.array(vec[2]))
        
        m = row_limited_csc(mat)
        o = m.copy()
        p = m.copy()
        q = m.copy()
        
        n = 3000
        
        end = np.zeros((4, 10), float)
        for j in range(10):
        
            start = time()
            for i in range(n):
                m.append(vec, fast=True)
            end[0][j] = time() - start
            
            start = time()
            for i in range(n):
                q.append(vec, fast=False)
            end[1][j] = time() - start
            
            vec_csc = ss.csc_matrix(vec)
            start = time()
            for i in range(n):
                o.append_csc(ss.csc_matrix(vec), fast=True)
            end[2][j] = time() - start
            
            #vec_csc = ss.csc_matrix(vec)
            start = time()
            for i in range(n):
                p.append_csc(ss.csc_matrix(vec), fast=False)
            end[3][j] = time() - start
            
            print(j)
        print(end)

 
    def override(self, vector, column):
        # Diese Funktion überschreibt die angegebene Spalte
        # Ist der angegebene Vector ungültig wird ein ValueError wegen gescheitertem Broadcasting geworfen.
        # Diese Funktion kann ebenfalls eine schnelle Version erhalten, in der nicht mit Nullen aufgefüllt wird.
        
        (data, indices) = vector

        # Setze die Korrekte Form
        maximum = max(indices)
        if maximum >= self.shape[0]:
            self._shape = (maximum + 1, self.shape[1])
        else:
            self._shape = (self.shape[0], self.shape[1])
        
        # Stelle die Korrekte Form sicher
        bf_ind, bf_data = self._backfilling(indices)
        
        # Setze die Matrix
        self.indices[self.indptr[column] : self.indptr[column + 1]] = np.concatenate([indices, bf_ind])
        self.data[self.indptr[column] : self.indptr[column + 1]] = np.concatenate([data, bf_data])
        
    
    
    
    
if __name__ == "__main__":
    from time import time
    msg.state("Start")
    stat = statik()
    #print(stat.ecken_ans)
    #print(stat.ecken_res)
    #print(stat.kanten_res)
    #print(stat.struktur_matrix.toarray())
    
    # (data, indices, indptr)
    
    
    
    
        
    #m.override(([3, 3, 3, 3, 3, 3], [0, 1, 2, 3, 4, 5]), 3)
    #print(m.toarray())
    
    
    
    
    