# main.py
import webuntis
import datetime
import os

from dotenv import load_dotenv

# LOGIN
load_dotenv()
NAME = os.getenv('NAME')
PASS = os.getenv('PASSKEY')

s = webuntis.Session(
    username=str(NAME),
    password=str(PASS),
    server='neilo.webuntis.com',
    school='Wilhelm-Raabe-Schule%20Lueneburg',
    useragent='WebUntis Test'
).login()

# DEFINE
today = datetime.date.today()
mo = today - datetime.timedelta(days=today.weekday())
tu = mo + datetime.timedelta(days=1)
date = datetime.datetime
timetable = {
    date(mo.year, mo.month, mo.day, hour=8, minute=0): "1. Stunde",
    date(mo.year, mo.month, mo.day, hour=8, minute=50): "2. Stunde",
    date(mo.year, mo.month, mo.day, hour=9, minute=55): "3. Stunde",
    date(mo.year, mo.month, mo.day, hour=10, minute=45): "4. Stunde",
    date(mo.year, mo.month, mo.day, hour=11, minute=45): "5. Stunde",
    date(mo.year, mo.month, mo.day, hour=12, minute=35): "6. Stunde",
}


def check(ch):
    return ch[:3]


# Assign Room ID and Room Name to dictionary 'raum'
raum = {}
for f in s.rooms():
    raum[f.name] = f.id
raumrev = {key: value for (value, key) in raum.items()}

# Only for Testing
# for key, value in raum.items():
#     print(key, ' : ', value)

# Assign Class ID and Class Name to dictionary 'klass'
klass = {}
for f in s.klassen():
    raum[f.name] = f.id
klassrev = {key: value for (value, key) in raum.items()}

foo = [[], [], []]
klassen = foo[0]
zeit = foo[1]
raume = foo[2]
i = 0
with open("data/neededrooms.txt") as idx:
    for f in idx:
        istrip = f.rstrip("\n")
        ida = raum.get(istrip)

        if f == 'stop':
            break

        for table in s.timetable(start=mo, end=mo, room=ida):
            klassen.append(table.klassen)
            zeit.append(timetable.get(table.start))
            raume.append(table.rooms)
            if table.start >= date(mo.year, mo.month, mo.day, 9, 55):
                if check(str(raume[i])) == '[R1':
                    print("Erstes Stockwerk!")
                if table.rooms.id == 17:
                    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
                    continue
                elif table.start > date(mo.year, mo.month, mo.day, 13, 20):
                    print("BBBBBBBBBBBBBBBBBB")
                    continue
                else:
                    print("Klasse", table.klassen, "hat in der", timetable.get(table.start), "in", table.rooms,
                          "unterricht.")
            i += 1

s.logout()
