
""" Dynamik...
"""

from dynamik_events import dynamik_events

class dynamik:
    
    def __init__(self):
        aktuelle_events = dynamik_events(dynamik_events(None))
    
    def durchlaufe_events(self):
        aktuelle_events.durchlaufe_events()
        
        aktuelle_events = aktuelle_events.zukünftige_events
        aktuelle_events.zukünftige_events = dynamik_events(None)
        