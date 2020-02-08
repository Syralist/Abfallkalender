from bs4 import BeautifulSoup
from ics import Calendar, Event
import re
import arrow
from dateutil import tz
import datetime

###### Einstellungen ######
# Html-Datei von der Eno
html = r"Abfallkalender von Entsorgung-kommunal.html"
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
offset_string = f" !!{offset_hours:02d}:00"
re_year = re.compile(r"[a-zA-z]*\s*(\d{4})$")
re_date = re.compile(r"(?:\(\w{2}\)\s)?(\d{2})\.(\d{2})\.\s*([\w\ \/\.]*)$")

# globale Variablen vorbelegen
year = None
c = Calendar()

## Datei öffnen
with open(html) as f:
    # HTML parsen
    soup = BeautifulSoup(f, "lxml")
    # Tabelle auswählen und über die Zeilen und Spalten iterieren
    rows = soup.find("table").find("tbody").find_all("tr")
    for row in rows[8:]:
        cells = row.find_all("td")
        for cell in cells:
            try:
                # Die Zelle mit den Terminen suchen
                if "top" in cell["valign"]:
                    # Den Text in der Zelle durchsuchen
                    for line in cell.text.split('\n'):
                        # Das Jahr auslesen mit RegEx
                        year_match = re.match(re_year, line)
                        if year_match:
                            year = year_match.group(1)
                            print(year)
                        # Einen Termin auslesen mit RegEx
                        date_match = re.match(re_date, line)
                        if date_match:
                            # Datum und Text auslesen
                            day = date_match.group(1)
                            month = date_match.group(2)
                            item = date_match.group(3)
                            print(day, month, item)
                            # Event anlegen
                            e = Event()
                            # Titel zusammenbauen
                            e.name = f"Müllabfuhr{(' ' + item) if descriptive_title else ''}{offset_string if offset_hours > 0 else ''}"
                            # Startzeitpunkt zusammenbauen
                            begin = arrow.get(datetime.datetime(int(year), int(month), int(day), event_hour, 0, 0, 0, tz.gettz("Europe/Berlin")))
                            if ics_workaround:
                                begin = begin.shift(days = 1)
                            e.begin = begin.shift(days = -1 if on_day_before else 0)
                            # Dauer eintragen bzw. ganztägigen Termin erzeugen
                            e.duration = {"hours": duration_hour}
                            if all_day:
                                e.make_all_day()
                            # Art der Abfuhr eintragen
                            e.description = item
                            # Event eintragen
                            c.events.add(e)
            except KeyError:
                # Tabellenzellen ohne Termine ignorieren
                continue

# Kalenderdatei schreiben
with open("abfuhr.ics", "w") as f:
    f.writelines(c)
