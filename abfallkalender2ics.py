from bs4 import BeautifulSoup
from ics import Calendar, Event
import re
import arrow
from dateutil import tz
import datetime

html = r"Abfallkalender von Entsorgung-kommunal.html"

year = None

re_year = re.compile(r"[a-zA-z]*\s*(\d{4})$")
re_date = re.compile(r"(?:\(\w{2}\)\s)?(\d{2})\.(\d{2})\.\s*([\w\ \/\.]*)$")

c = Calendar()

with open(html) as f:
    soup = BeautifulSoup(f, "lxml")
    rows = soup.find("table").find("tbody").find_all("tr")
    i = 0
    for row in rows[8:]:
        i += 1
        # print(row)
        cells = row.find_all("td")
        for cell in cells:
            try:
                if "top" in cell["valign"]:
                    for line in cell.text.split('\n'):
                        year_match = re.match(re_year, line)
                        if year_match:
                            year = year_match.group(1)
                            print(year)
                        date_match = re.match(re_date, line)
                        if date_match:
                            day = date_match.group(1)
                            month = date_match.group(2)
                            item = date_match.group(3)
                            print(day, month, item)
                            e = Event()
                            e.name = "#muellabfuhr"
                            begin = arrow.get(datetime.datetime(int(year), int(month), int(day), 18, 0, 0, 0, tz.gettz("Europe/Berlin")))
                            e.begin = begin.shift(days=-1)
                            e.duration = {"hours": 1}
                            e.description = item
                            # print(e)
                            c.events.add(e)
            except KeyError:
                continue
        # if i > 3:
        #     break

# print(c.events)

with open("abfuhr.ics", "w") as f:
    f.writelines(c)
