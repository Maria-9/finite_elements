
"""Jedes Element, das der Statik hinzugefügt wird, muss nummeriert sein, damit seine Position im entsprechenden Array eindeutig festgelegt wird."""

class nummeriert:
    """ 
    Beschreibung:
        Jedes Element, das der Statik hinzugefügt wird, muss nummeriert sein, damit seine Position im entsprechenden Array des Statik-Objektes eindeutig festgelegt wird.
    
    
    Öffentliche Methoden:
        nummeriert_als(cls) -> Gibt True zurück, falls das class-Attribut des aufrufenden Objektes obj.__class__ = cls der übergebenen Klasse cls ist.
    
    Vererbte Methoden:
        __init__()  -> weist dem Objekt eine neue Nummer zu.
        __del__()   -> gibt die Nummer des Objektes frei, so dass die neue Nummer später an eine neue Instanz vergeben werden kann.
    
    
    Bemerkung:
        Eine andere Klasse kann in die nummierierung einer Klasse mit aufgenommen werden, indem das __class__ Attribut gleich gesetzt wird.
        (Dies beeinflusst das Ergebnis von type(obj) nicht.)
    """

    __freie_nummern = list()
    __höchste_nummer = 0
    
    @classmethod
    def __neue_nummer(cls):
        if len(cls.__freie_nummern) == 0:
            cls.__höchste_nummer += 1
            return cls.__höchste_nummer - 1
        else:
            return cls.__freie_nummern.pop()
    
    def __init__(self):
        self.nummer = self.__class__.__neue_nummer()
    
    def __del__(self):
        self.__class__.__freie_nummern.append(self.nummer)
    
    def __str__(self):
        return "\n Nummer: " + str(self.nummer) + "\t[" + self.__class__.__name__ + "]"
    
    def nummeriert_als(self, cls):
        return self.__class__ == cls
 