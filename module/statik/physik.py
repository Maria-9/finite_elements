
""" Diese Klasse implementiert alle physikalischen Gesetzmäßigkeiten mithilfe der drei Module:
        statik
        dynamik
        korrektur
"""

from .statik import statik
from .dynamik import dynamik
from .korrektur import korrektur
from .sphäre import sphäre

class physik:
    
    def __init__(self, num_ecken, num_kanten, dim = 2):
        self.statik = statik(num_ecken, num_kanten, dim)
        self.dynamik = dynamik()
        self.korrektur = korrektur()
        
        self.container = container()
    
        """
        """