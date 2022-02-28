
""" ClassConverter ist eine Metaklasse zum erstellen von Klassen, deren ausschließlicher Zweck es ist Klassen in andere Klassen zu konvertieren.
    Gebrauch:
        class testclass(metaclass=ClassConverter):
            
            @classmethod
            def __convert__Classname1(cls, convert):
                ...
                return Converted_convert
            
            @classmethod
            def __convert__Classname2(cls, convert):
                ...
                return Converted_convert
            
            ...
         converted_class = testclass(Classname1)
    
    Bemerkungen:
        Es ist nicht möglich Instanzen von Klassen, die vom Typ ClassConverter sind zu erzeugen.
        Aus diesem Grund müssen alle Methoden als @classmethod deklariert werden.
"""

class ClassConverter(type):

    def __call__(cls, *args, **kwargs):
    
        @classmethod
        def __no_conversion_defined(cls, convert):
            print("__convert__" + convert.__name__)
            raise Exception(str(cls) + " has no conversion for class " + convert.__name__ + " defined.")
        
        setattr(cls, "__no_conversion_defined", __no_conversion_defined)
        
        @classmethod
        def __convert__(cls, convert):
            if convert.__name__ in cls.__dict__:
                return cls.__dict__[convert.__name__]
            setattr(cls, convert.__name__, getattr(cls, "_" + cls.__name__ + "__convert__" + convert.__name__, __no_conversion_defined)(convert))
            return cls.__dict__[convert.__name__]
            
        setattr(cls, "__convert__", __convert__)
        
        return cls.__convert__(args[0])
