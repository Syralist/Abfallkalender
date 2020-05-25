Dieses Python Skript erzeugt eine ICS Kalenderdatei mit den Müllabfuhrterminen der Bremer Stadtreinigung.

# Vorbereitung
Auf der Homepage der Bremer Stadtreiniung [(Direktlink)](https://www.die-bremer-stadtreinigung.de/privatkunden/entsorgung/bremer_abfallkalender-23080) wählt man seine Adresse aus und bekommt dann eine Seite mit den Abfuhrterminen als Tabelle angezeigt. Zusätzlich hat man jetzt die Option die Termine als iCal und CSV herunterzuladen.
Die CSV Datei im gleichen Verzeichnis ablegen wo auch das Python Skript liegt.

# Konfiguration
Oben im Python Skript lassen sich einige Dinge konfigurieren:
* Soll die Art der Abfuhr in den Titel eingetragen werden? True/False
* Soll für die HomeAssistant Integration ein Offset eingetragen werden? 0..23
* Soll ein ganztägiger Termin erzeugt werden? True/False
* Workaround für fehlerhafte All Day Events in ics.py aktivieren? True/False
* Soll der Termin am Tag vor der Abfuhr erzeugt werden? True/False
* Zu welcher Stunde der Termin erzeugt werden, wenn er nicht ganztägig ist? 0..23
* Wie lange soll der Termin sein, wenn er nicht ganztägig ist? 0..23

# Kompatibilität
Python >=3.6

getestet mit dem Abfallkalender 2020 bis 2021

Import der ics-Datei getestet mit Google Kalender