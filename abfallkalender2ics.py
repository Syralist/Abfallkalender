import csv
from ics import Calendar, Event
import re
import arrow
from dateutil import tz
import datetime

###### Einstellungen ######
# CSV-Datei von der Eno
csv_file = r"Abfuhrtermine für  Auf dem Kamp.csv"
# Soll die Art der Abfuhr in den Titel eingetragen werden? True/False
descriptive_title = True
# Soll für die HomeAssistant Integration ein Offset eingetragen werden? 0..23
offset_hours = 6
# Soll ein ganztägiger Termin erzeugt werden? True/False
all_day = True
# Workaround für fehlerhafte All Day Events in ics.py aktivieren? True/False
ics_workaround = True
# Soll der Termin am Tag vor der Abfuhr erzeugt werden? True/False
on_day_before = False
# Zu welcher Stunde der Termin erzeugt werden, wenn er nicht ganztägig ist? 0..23
event_hour = 18
# Wie lange soll der Termin sein, wenn er nicht ganztägig ist? 0..23
duration_hour = 1
######

# Hilfsvariablen
offset_string = f" !!-{offset_hours:02d}:00"

# globale Variablen vorbelegen
d = {}
c = Calendar()

## Datei öffnen
with open(csv_file) as f:
    # CSV parsen
    csv_reader = csv.reader(f, delimiter=';', quotechar='"')
    for row in csv_reader:
        if row[0] == 'Wochentag':
            # Überschrift überspringen
            continue
        # Mehrere Abfuhren an einem Tag zusammenfassen
        if row[1] in d:
            d[row[1]] =f"{d[row[1]]} / {row[2]}"
        else:
            d[row[1]] = row[2]

# Zusammengefasste Termine ins ICS Format umandeln
for datum, abfuhr in d.items():
    # Event anlegen
    e = Event()
    # Titel zusammenbauen
    e.name = f"Müllabfuhr{(' ' + abfuhr) if descriptive_title else ''}{offset_string if offset_hours > 0 else ''}"
    # Startzeitpunkt zusammenbauen
    _date = datetime.datetime.strptime(datum, "%d.%m.%Y").replace(hour=event_hour, tzinfo=tz.gettz("Europe/Berlin"))
    begin = arrow.get(_date)
    if ics_workaround:
        begin = begin.shift(days = 1)
    e.begin = begin.shift(days = -1 if on_day_before else 0)
    # Dauer eintragen bzw. ganztägigen Termin erzeugen
    e.duration = {"hours": duration_hour}
    if all_day:
        e.make_all_day()
    # Art der Abfuhr eintragen
    e.description = abfuhr
    # Event eintragen
    c.events.add(e)


# Kalenderdatei schreiben
with open("abfuhr.ics", "w") as f:
    f.writelines(c)
