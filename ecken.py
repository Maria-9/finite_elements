
# Elementare Klassen der Finiten Elemente Analyse

# --------------
# Beim überarbeiten des Moduls sollte auf eine einheitliche Schreibweise von indizes und indices geachtet werden.


# Im folgenden Ordner ist das 'messagebox' Modul gespeichert.
import sys
sys.path.insert(1, 'C:\\Users\\Sebastian Hahn\\AppData\\Roaming\\Notepad++\\plugins\\config\\PythonScript\\npp_environment')

import numpy as np
from messagebox import msg
import scipy.sparse as ss
import matplotlib.patches as patches
import matplotlib.path as path
import matplotlib.pyplot as plt
from scipy.sparse.linalg import lsqr


class nummeriert:
    # sollen zwei unterschiedliche Klassen in die selbe Nummerierung aufgenommen werden, so kann das __class__ Attribut manuell gleich gesetzt werden.
    # type(obj) wird von der manuellen Setzung von __class__ nicht beeinflusst. 
    # Eventuell ist es dann aber auch schöner dies von einer Art _kind abhängig zu machen, finde allerdings die Implementierung mit __class__ ganz gut.

    __freie_nummern = list()
    __höchste_nummer = 0
    _kind = "nummeriertes_objekt"   # überschreibe dies - _kind dient ausschließlich zur besseren Lesbarkeit auf der Konsole
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
    
    def __del__(self):
        self.__class__.__freie_nummern.append(self.nummer)
    
    def __str__(self):
        return "\n Nummer: " + str(self.nummer) + "\t[" + self.__class__._kind + "]"
    
    def nummeriert_als(self, cls):
        return self.__class__ == cls
    
class statik:
    
    def __init__(self, num_ecken, num_kanten, dim = 2):
        self.dim = dim                                  # die Dimension in der sich die Statik bewegt.
        self.ecken_ans = np.zeros(num_ecken*self.dim)   # die an den Eckpunkten ansetzenden Kräfte e_a
        self.ecken_res = np.zeros(num_ecken*self.dim)   # die an den Eckpunkten resultierenden Kräfte nach der berechnung e_r = e_a + S * k_r
        self.kanten_res = np.zeros(num_kanten)          # die an den Kanten resultierenden Kräfte k_r = S^(-1) * e_a
        self.struktur_matrix = row_limited_csc.empty(2*self.dim, len(self.kanten_res), dtype=float)      # die Strukturmatrix.
  
    def inkludiere(self, obj):
        
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
        
        # obj == Kante
        if obj.nummeriert_als(kante):
            
            # berechne die Kräfteverteilung auf die Ecken 
            # (- also die zur Kante gehörige Spalte in der Strukturmatrix.)
            
            vec = [list(), list()] # indizes, daten
            for e in [obj.ecke1, obj.ecke2]:
                if type(e) != statische_ecke:
                    vec[0].extend([e.nummer * self.dim + i for i in range(self.dim)])
                    vec[1].extend(e.richtung_von(obj.gib_nachbar(e)))
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
                if self.kanten_res[obj.nummer] != 0:
                    msg.warning("Der Speicherplatz auf den die neue Kante zugreift war ungleich 0.")
                
                # trage die Kräfteverteilung in die Strukturmatrix ein.
                self.struktur_matrix.override((vec[1], vec[0]), obj.nummer)
        
    def exkludiere(self, obj):
        # obj == Ecke
        if obj.nummeriert_als(dynamische_ecke):
            i = [obj.nummer * self.dim + i for i in range(self.dim)]
            self.ecken_ans[i] = [0] * self.dim  
            self.ecken_res[i] = [0] * self.dim

        # obj == Kante
        if obj.nummeriert_als(kante):
            self.kanten_res[obj.nummer] = 0
            self.struktur_matrix.override(([0]*2*self.dim, [i for i in range(2*self.dim)])) # Diese Zeile ist sehr wichtig.

    def berechne(self):
        # a := ecken_ans
        # e := ecken_res
        # S := struktur_matrix
        # r := kanten_res
        
        # es gibt eine neue ansetzende Kraft a.
        # minimiere über r die Norm von
        # e = Sr + a = S*dr + (a + S*r_0)
        # dies entspricht dem Lösen des least-aquares Problem von S*dr = -a - S*r_0
        # mit r = dr + r_0, wobei r_0 die alte resultierende Kraft ist.
        
        # Die Rechengeschwindigkeit kann ev. verbessert werden, indem (- self.ecken_ans - self.struktur_matrix.dot(self.kanten_res))
        # in ein ss.bsr_array gecaset wird. (Ist hierfür eine neue Version von scipy notwendig?)
        # Des weiteren könnte der lsrq - Optimierer durch eine eigene Version verschnellert werden, indem eine sparse List of List - Matrix mitgeführt.
        # Über diese könnte für jede Knotenkraft, die sich verändert hat, die Kanten ermittelt werden, über die eine Optimierung notwendig ist.
        
        erg = lsqr(self.struktur_matrix, - self.ecken_ans - self.struktur_matrix.dot(self.kanten_res),
                       damp = 0, atol = 0.001, iter_lim = 1000, show = True)
        dr = erg[0]
        self.kanten_res = dr + self.kanten_res
        self.ecken_res = self.struktur_matrix.dot(self.kanten_res) + self.ecken_ans
        
        msg.info("Statik Berechnung:\n" +
                   " Gestoppt bei Iteration: " + str(erg[2]) + "\n" +
                   " 1-Norm der Abweichung: " + str(erg[3]))
        
        

class ecke(nummeriert):

    # __slots__ = ['nummer', 'dynamisch', 'position', 'ansetzende_kraft', 'resultierende_kraft', 'masse', kanten', 'nachbarn']
    _kind = "Ecke"
    
    def __init__(self, position):
        super().__init__() # Gebe dem Objekt eine Nummer
        
        self.position = np.array(position)
        self.dim = len(position)
        self.kanten = list()        # Wozu gibt es hier eigentlich Kanten und Nachbarn - sollte eine Liste mit Kanten nicht ausreichen?
        self.nachbarn = list()
    
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
    
    def richtung_von(self, andere_ecke):
        # gibt den Richtungsvektor zurück.
        x = self.position - andere_ecke.position
        return x / np.sqrt(x @ x)
    
    def __str__(self):
        return ("----------------------------"
                + super().__str__() # dies ist die Nummerierung
                + "\n Position: " + str(self.position)
                + "\n Kanten : " + str([k.nummer for k in self.kanten])
                + "\n Nachbarn : " + str([n.nummer for n in self.nachbarn]))

    def verts_codes(self, size = 0.1):
        if self.dim != 2:
            raise Exception("Diese Funktion ist nur für 2-D Plots erstellt worden.")
        
        verts = [self.position + np.array([1, 0])*size,
                self.position + np.array([0, 1])*size,
                self.position + np.array([-1, 0])*size,
                self.position + np.array([0, -1])*size,
                self.position + np.array([1, 0])*size]
        
        codes = [path.Path.MOVETO,
                path.Path.LINETO,
                path.Path.LINETO,
                path.Path.LINETO,
                path.Path.CLOSEPOLY]
        
        return (verts, codes)


class dynamische_ecke(ecke):
    
    _kind = "dynamisch"
    
    def __init__(self, position, statik, ans_kraft = "DEFAULT"):
        if ans_kraft == "DEFAULT":
            ans_kraft = [0 for i in position[0:-1]] + [-1]
            
        
        super().__init__(position)
        self.masse = None # Die Masse spielt erst bei Bewegungen eine Rolle
        
        if statik.dim != self.dim:
            raise ValueError("Ein " + statik.dim + " dimensionales Statik-Objekt kommt nicht mit einer " + self.dim + " dimensionalen Ecke zurecht.")

        self.statik = statik
        self.statik.inkludiere(self)
        
        # Dies sind Attribute die auf den Speicher im Objekt self.statik zurückgreifen.
        self.setze_ans_kraft = ans_kraft
        self.setze_res_kraft = 0
    
    def __del__(self): 
        self.statik.exkludiere(self)
        super().__del__()
    
    def __stat_sp(self):
        # Gibt den Speicherbereich für die Kräfte im Statik Objekt zurück.
        return [self.nummer*self.dim + i for i in range(self.dim)]
    
    @property
    def ans_kraft(self):
        return self.statik.ecken_ans[self.__stat_sp()]
    
    @ans_kraft.setter
    def setze_ans_kraft(self, ans_kraft):
        self.statik.ecken_ans[self.__stat_sp()] = ans_kraft
        
    @property
    def res_kraft(self):
        return self.statik.ecken_res[self.__stat_sp()]
    
    @res_kraft.setter
    def setze_res_kraft(self, res_kraft):
        self.statik.ecken_res[self.__stat_sp()] = res_kraft
        
    def __str__(self):
        return (super().__str__()
                + "\n Masse : " + str(self.masse)
                + "\n Ansetzende Kraft: " + str(self.ansetzende_kraft)
                + "\n Resultierende Kraft: " + str(self.resultierende_kraft))
    
    def verts_codes_color(self):
        verts, codes = self.verts_codes()
        
        color = (0, 1 - 1/(np.linalg.norm(self.res_kraft) + 1), 0.1)
        
        return verts, codes, color

class statische_ecke(ecke):
    # statische Ecken tragen sich nicht in der statik ein.
    # statische Ecken dienen lediglich als Fixpunkte.
    _kind = "statisch"
    
    def __init__(self, position):
        super().__init__(position)
    
    def verts_codes_color(self):
        verts, codes = self.verts_codes()
        
        color = (0, 0, 0)

        return verts, codes, color


class kante(nummeriert):

    _kind = "Kante"
    
    def __init__(self, ecke1, ecke2, statik, kraft_limit=10):
        
        super().__init__()
        self.kraft_limit = kraft_limit

        self.ecke1 = ecke1
        self.ecke2 = ecke2

        self.ecke1.neue_kante(self)
        self.ecke2.neue_kante(self)
        
        self.statik = statik
        self.statik.inkludiere(self)

    
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
    
    @property
    def res_kraft(self):
        return self.statik.kanten_res[self.nummer]
    
    @res_kraft.setter
    def setze_res_kraft(self, res_kraft):
        self.statik.kanten_res[self.nummer] = res_kraft
        
    def __del__(self):
        msg.info("Shall I get deleted?")
        self.statik.exkludiere(self)
        super().__del__()
          
    def __str__(self):
        return (super().__str__()
                + "\n Ecken: [" + str(self.ecke1.nummer) + ", " + str(self.ecke2.nummer) + "]")
            
    def verts_codes_color(self):
        if self.ecke1.dim != 2 or self.ecke2.dim != 2:
            raise Exception("Diese Funktion ist nur für 2-D Plots erstellt worden.")
        
        verts = [self.ecke1.position, self.ecke2.position]
        
        codes = [path.Path.MOVETO,
                path.Path.LINETO]
        
        color = [0, 0, 0] # RGB
        if self.res_kraft > 0:
            color[0] = min(1, self.res_kraft / self.kraft_limit)
        else:
            color[2] = min(1, -self.res_kraft / self.kraft_limit)
        
        return (verts, codes, color)

    
class row_limited_csc(ss.csc_matrix):
    
    # Es ist sehr wichtig den Datentyp mit anzugeben - Float Werte werden feherhaft oder gar nicht in eine csc-Matrix mit Integer-Werten übernommen.

    @staticmethod
    def empty(num_rows, num_cols, shape=None, dtype=None):
        return row_limited_csc(([0]*num_rows*num_cols, [i for i in range(num_rows)]*num_cols, [i*num_rows for i in range(num_cols+1)]), shape=shape, dtype=dtype)
    
    def __init__(self, arg1, num_rows=None, shape=None, dtype=None, copy=False):
        
        # das Argument shape wird benötigt, da ein Konstruktor für eine csc_matrix stets diesen Parameter nimmt. Würde er fehlen, könnte scipy nicht regelkonform
        # mit dieser Klasse rechnen können. Der Parameter erfüllt hier jedoch keinen weiteren Sinn.
        
        # @docstring:
        # Die angegebene Matrix wird vergrößert, falls sie weniger Zeilen enthält als angegeben.
        # Sie wird niemals verkleinert.
        
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


class matplot:
    def __init__(self, shape=(8,8)):
        self.fig, self.ax = plt.subplots()
        self.shape = shape
      
    def add(self, objects):
        for obj in objects:
            verts, codes, color = obj.verts_codes_color()
            obj_path = path.Path(verts, codes)
            patch = patches.PathPatch(obj_path, facecolor=color,
                                    edgecolor=color, alpha=0.5)
            self.ax.add_patch(patch)
    
    def show(self):
        maximum = 8
        self.ax.set_xlim(0, self.shape[0])
        self.ax.set_ylim(0, self.shape[1])
        
        plt.show()

    
class universe:
    
    def __init__(self):
        höhe_turm = 5
        länge_überhang = 2
        num_ecken = 2*(höhe_turm + länge_überhang) + 1
        num_kanten = 2 * num_ecken 
        #self.stat = statik(num_ecken, num_kanten) # Je genauer die Werte für num sind, desto weniger Rechenzeit wird zum Aufbau benötigt.
        self.stat = statik(1, 1)
        self.st_ecken = list()
        self.ecken = list()
        self.kanten = list()
        self.mplot = matplot()
        
        #baue den Turm
        for i in range(höhe_turm*2):
            if i % 2 == 0:
                e = dynamische_ecke((1, i / 2 + 1), self.stat)
            else:
                e = dynamische_ecke((2, (i+1) / 2), self.stat)
            self.ecken.append(e)
        
        #setze Eckpunkt
        self.ecken.append(dynamische_ecke((2, höhe_turm+1), self.stat))
        
        #baue nach rechts
        for i in range(2*länge_überhang):
            if i % 2 == 0:
                e = dynamische_ecke((3 + i/2, höhe_turm), self.stat)
            else:
                e = dynamische_ecke((2 + (i+1)/2, höhe_turm + 1), self.stat)
            self.ecken.append(e)
        
        #setze zwei statischen Ecken am Boden
        prev_2 = statische_ecke((1, 0))
        prev_1 = statische_ecke((2, 0))
        
        self.st_ecken.extend([prev_2, prev_1])
        
        #setze die Kanten
        for e in self.ecken:
            
            self.kanten.append(kante(prev_2, e, self.stat))
            self.kanten.append(kante(prev_1, e, self.stat))
            
            prev_2 = prev_1
            prev_1 = e

        
    def plot(self):
        
        for obj in [self.ecken, self.st_ecken, self.kanten]:
            self.mplot.add(obj)
        
        self.mplot.show()

    
    def run(self):
        self.stat.berechne()
        self.plot()

if __name__ == "__main__":
    
    msg.state("Start")
    uni = universe()
    uni.run()
    
    print(uni.stat.ecken_ans)
    print(uni.stat.kanten_res)
    
    
    
    
    
    