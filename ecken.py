
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
    
    def __init__(self, dim = 2, ecken_ans = np.array([0]), ecken_res = np.array([0]), kanten_res = np.array([0])):
        self.dim = dim                          # die Dimension in der sich die Statik bewegt.
        self.ecken_ans = ecken_ans              # die an den Eckpunkten ansetzenden Kräfte e_a
        self.ecken_res = ecken_res              # die an den Eckpunkten resultierenden Kräfte nach der berechnung e_r = e_a + S * k_r
        self.kanten_res = kanten_res            # die an den Kanten resultierenden Kräfte k_r = S^(-1) * e_a
        self.struktur_matrix = row_limited_csc(([0], [0], [0,0]), dtype=float)      # die Strukturmatrix.
        
    def neue_kante(self, kante):
        #self.strukturmatrix = hstack(self.struktur_matrix, kante.)
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
    
    def __init__(self, arg1, num_rows=None, dtype=None, copy=False):
            
        ss.csc_matrix.__init__(self, arg1, dtype=dtype, copy=copy)
        
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
        
        # correct the format of the matrix.
        
        new_data = []
        new_indices = []
        new_indptr = []
        
        prev_ptr = 0
        for ptr in self.indptr:
            if ptr == 0:
                continue
            new_data.extend(self.data[prev_ptr : ptr])
            new_data.extend([0 for i in range(self.num_rows - (ptr - prev_ptr))])
            
            
            new_indices.extend(self.indices[prev_ptr : ptr])
            #new_indizes.extend([i for i in set(range(num_rows))...])
                # Es sollen die Indizes von unten aufgefüllt werden, jedoch nicht die aus self.indizes[prev_ptr : ptr] doppelt vorkommen.
            
        
        

        # data, indizes, inptr sollten am Ende numpy arrays sein.
        self._shape = (1, 1) # Correct this!
            

        # elif isinstance(arg1, tuple):
            # if isshape(arg1):
                # # It's a tuple of matrix dimensions (M, N)
                # # create empty matrix
                # self._shape = check_shape(arg1)
                # M, N = self.shape
                # # Select index dtype large enough to pass array and
                # # scalar parameters to sparsetools
                # idx_dtype = get_index_dtype(maxval=max(M, N))
                # self.data = np.zeros(0, getdtype(dtype, default=float))
                # self.indices = np.zeros(0, idx_dtype)
                # self.indptr = np.zeros(self._swap((M, N))[0] + 1,
                                       # dtype=idx_dtype)
            # else:
                # if len(arg1) == 2:
                    # # (data, ij) format
                    # other = self.__class__(
                        # self._coo_container(arg1, shape=shape, dtype=dtype)
                    # )
                    # self._set_self(other)
                # elif len(arg1) == 3:
                    # # (data, indices, indptr) format
                    # (data, indices, indptr) = arg1

                    # # Select index dtype large enough to pass array and
                    # # scalar parameters to sparsetools
                    # maxval = None
                    # if shape is not None:
                        # maxval = max(shape)
                    # idx_dtype = get_index_dtype((indices, indptr),
                                                # maxval=maxval,
                                                # check_contents=True)

                    # self.indices = np.array(indices, copy=copy,
                                            # dtype=idx_dtype)
                    # self.indptr = np.array(indptr, copy=copy, dtype=idx_dtype)
                    # self.data = np.array(data, copy=copy, dtype=dtype)
                # else:
                    # raise ValueError("unrecognized {}_matrix "
                                     # "constructor usage".format(self.format))

        # else:
            # # must be dense
            # try:
                # arg1 = np.asarray(arg1)
            # except Exception as e:
                # raise ValueError("unrecognized {}_matrix constructor usage"
                                 # "".format(self.format)) from e
            # self._set_self(self.__class__(
                # self._coo_container(arg1, dtype=dtype)
            # ))

        # # Read matrix dimensions given, if any
        # if shape is not None:
            # self._shape = check_shape(shape)
        # else:
            # if self.shape is None:
                # # shape not already set, try to infer dimensions
                # try:
                    # major_dim = len(self.indptr) - 1
                    # minor_dim = self.indices.max() + 1
                # except Exception as e:
                    # raise ValueError('unable to infer matrix dimensions') from e
                # else:
                    # self._shape = check_shape(self._swap((major_dim,
                                                          # minor_dim)))

        # if dtype is not None:
            # self.data = self.data.astype(dtype, copy=False)

        # self.check_format(full_check=False)


    def append_col(self, column):
            
        pass
            
    
    
    
    
if __name__ == "__main__":
    msg.state("Start")
    stat = statik()
    print(stat.ecken_ans)
    print(stat.ecken_res)
    print(stat.kanten_res)
    print(stat.struktur_matrix.toarray())
    
    # (data, indices, indptr)
    m = ss.csc_matrix(([1, 2, 3, 4, 5, 6, 7, 8, 9],[0, 4, 8, 0, 4, 8, 0, 4, 8],[0, 2, 4, 6, 8, 9]))
    print(m.toarray())
    print(m.shape)
    
    
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
    
    
    
    
    