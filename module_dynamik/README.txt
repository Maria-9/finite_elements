Dieses dynamik-Modul berechnet die korrekte Verteilung der in einem Gitter vorhandenen Punkte indem die klassischen physikalischen Gesetze 
über Stauchung / Dehnung, Beschleunigung und Geschwindigkeit innerhalb des Gitters verwendet werden. Für eine bessere Konvergenz sind 
diese Gesetze abgewandelt worden. Die Konvergenz eines Gitters mit 40 Punkten kann dennoch 10 Sekunden in Anspruch nehmen. Dies zeigt den
Nachteil dieser Implementierung sehr deutlich. Ein Vorteil könnte sein, dass die Berechnungsdauer mit Zunahme der Punkte geschätzt lediglich
Logarithmisch zunimmt. 
Es lässt sich annehmen, dass diese Art der Implementierung später für größere sichtbare Bewegungen gute Resultate liefert, jedoch für die
Feinjustierung der Kräfteverteilung in einem Netz nicht geeignet ist. Aus diesem Grund wird dieser Ansatz hier nicht weiter verfolgt.