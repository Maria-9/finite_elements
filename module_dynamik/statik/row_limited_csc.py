
""" Eine Zeilen-beschränkte CSC-Matrix wird zur Berechnung der Statik verwendet. 
    Sie ist dahingehend optimiert, dass es die Zeilenanzahl beschränkt ist, wodurch das schnelle verändern von Spalten gewährleistet wird."""
    
import numpy as np
import scipy.sparse as ss
from messagebox import msg
   
class row_limited_csc(ss.csc_matrix):
    """ 
    Eine row_limited_csc hat die folgende Form einer csc-Matrix, wobei n = num_rows die maximale Anzahl der Zeilen, die ungelich Null sein können angibt.
    Die Indizes in 'indices' müssen weder geordnet sein, noch müssen die Einträge bzw. der Daten ungleich Null sein. Jedoch müssen pro Spalte genau n Indizes geführt werden.
    
    data :=     [x00, x10, x20, x30, ..., xn0, x01, x11, x21, x31, ..., xn1,  x02,  x12,  x22,  x32, ...,  xn2]
    indices :=  [ i0,  i1,  i2,  i3, ..., in,  i'0, i'1, i'2, i'3, ..., i'n, i''0, i''1, i''2, i''3, ..., i''n]
    indptr:=    [  0,                      n,                            2n,                                3n]
    """
    
    # Es ist sehr wichtig den Datentyp mit anzugeben - Float Werte werden feherhaft oder gar nicht in eine csc-Matrix mit Integer-Werten übernommen.

    @staticmethod
    def empty(num_rows, num_cols, shape=None, dtype=None):
        return row_limited_csc(([0]*num_rows*num_cols, [i for i in range(num_rows)]*num_cols, [i*num_rows for i in range(num_cols+1)]), shape=shape, dtype=dtype)
    
    def __init__(self, arg1, num_rows=None, shape=None, dtype=None, copy=False):
        """ Die angegebene Matrix wird vergrößert, falls sie weniger Zeilen enthält als angegeben. Sie wird niemals verkleinert."""

        # das Argument shape wird benötigt, da ein Konstruktor für eine csc_matrix stets diesen Parameter nimmt. Würde er fehlen, könnte scipy nicht regelkonform
        # mit dieser Klasse rechnen können. Der Parameter erfüllt hier jedoch keinen weiteren Sinn.
        # Weiter unten kann full_check auf False gesetzt werden um Zeit zu sparen.
        
        if len(arg1) != 3:
            raise ValueError("row_limited_csc übernimmt als arg1 außschließlich Tupel der Länge 3 im Format (data, indices, indptr)")

        ss.csc_matrix.__init__(self, arg1, dtype=dtype, shape=shape, copy=copy)
        
        if self.dtype != float:
            msg.warning("Es wurde eine row_limited_csc-Matrix mit dem Datentyp " + str(self.dtype) + " erstellt.")
        
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
        """ Überprüft, ob in einer Spalte mehr als einmal ein Indize für die entsprechende Zeile verwendet wurde. """
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

    def append(self, triple, fast=False):
        """ Fügt die CSC_Matrix, die durch 'triple = (data, indices, indptr)' gegeben ist von rechts an.
            Vorsicht! Ist fast=True müssen die Eingabedaten bereits in der richtigen Form einer row_limited_csc sein."""

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

            # Prüfe die Korrektheit:
            self.check_format(full_check=False)
            
        else:
            csc = row_limited_csc(triple, num_rows=self.num_rows)
            csc = ss.hstack([self, csc])
            self._set_self(csc)

    def append_csc(self, csc_matrix, fast=False):
        """ Hängt die CSC_Matrix rechts an.
            Vorsicht! Ist fast=True müssen die Eingabedaten bereits in der richtigen Form einer row_limited_csc sein."""
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
        """ Diese Funktion überschreibt die angegebene Spalte 'column' mit dem Vektor 'vector'.
            Ist der angegebene Vektor ungültig wird ein ValueError wegen gescheitertem Broadcasting geworfen."""
        
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