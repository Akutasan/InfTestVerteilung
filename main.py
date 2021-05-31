import webuntis
import datetime
import os

from dotenv import load_dotenv

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

today = datetime.date.today()
mo = today - datetime.timedelta(days=today.weekday())
tu = mo + datetime.timedelta(days=1)

room1 = open("data/rooms.txt", 'w')
room2 = open("data/roomid.txt", 'w')
for i in s.rooms():
    room1.write(str(i) + "\n")
    room2.write(str(i.id) + "\n")
room1.close()
room2.close()

klass1 = open("data/klassen.txt", 'w')
klass2 = open("data/klassenid.txt", 'w')
for i in s.klassen():
    klass1.write(str(i) + "\n")
    klass2.write(str(i.id) + "\n")
klass1.close()
klass2.close()

raum = {}
r_temp = []
r_temp1 = []
with open("data/roomid.txt") as f:
    with open("data/rooms.txt") as t:
        for val in f:
            vals = val.rstrip("\n")
            r_temp.append(vals)
            for key in t:
                keys = key.rstrip("\n")
                r_temp1.append(keys)
        for i in range(len(r_temp)):
            raum[r_temp[i]] = r_temp1[i]
raumrev = {key: value for (value, key) in raum.items()}

klass = {}
k_temp = []
k_temp1 = []
with open("data/klassenid.txt") as f:
    with open("data/klassen.txt") as t:
        for val in f:
            vals = val.rstrip("\n")
            k_temp.append(vals)
            for key in t:
                keys = key.rstrip("\n")
                k_temp1.append(keys)
        for i in range(len(k_temp)):
            raum[k_temp[i]] = k_temp1[i]
klassrev = {value: key for (key, value) in klass.items()}

date = datetime.datetime


# for key, value in raumrev.items():
#     print(key, ' : ', value)

# print("ppp", raumrev.get('R312'))

# timetable = {
#     date(mo.today(), hour=8, minute=0): "1. Stunde",
#     date(mo, hour=8, minute=50): "2. Stunde",
#     date(mo, hour=9, minute=55): "3. Stunde",
#     date(mo, hour=10, minute=45): "4. Stunde",
#     date(mo, hour=11, minute=45): "5. Stunde",
#     date(mo, hour=12, minute=35): "6. Stunde",
# }


def con(dattim):
    if dattim is date(mo, hour=8, minute=0):
        return "1. Stunde"
    elif dattim is date(mo, hour=8, minute=50):
        return "2. Stunde"
    elif dattim is date(mo, hour=9, minute=55):
        return "3. Stunde"
    elif dattim is date(mo, hour=10, minute=45):
        return "4. Stunde"
    elif dattim is date(mo, hour=11, minute=45):
        return "5. Stunde"
    elif dattim is date(mo, hour=12, minute=35):
        return "6. Stunde"
    else:
        return "NonAns"


with open("data/neededrooms.txt") as i:
    for f in i:
        istrip = f.rstrip("\n")
        ida = raumrev.get(istrip)

        if f == 'stop':
            break
        elif istrip is None:
            continue

        for table in s.timetable(start=mo, end=mo, room=ida):
            if table.start >= date(2020, 5, 31, hour=8, minute=0):
                print(table.start, table.klassen, table.rooms, table.subjects)

# getthem = input("rin da: \n")
#
# if getthem in raum:
#     for tables in s.timetable(start=mo, end=mo, room=raum.get(getthem)):
#         print(tables)
#
# getthem2 = input("rini da: \n")
#
# if getthem2 in klass:
#     for tables in s.timetable(start=mo, end=mo, klasse=klass.get(getthem2)):
#         print(tables)

s.logout()
