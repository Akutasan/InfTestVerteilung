import webuntis
import datetime
import os

from dotenv import load_dotenv

load_dotenv()
NAME = os.getenv('NAME')
PASS = os.getenv('PASSKEY')

print(NAME, PASS)


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
with open("data/roomid.txt") as f:
    with open("data/rooms.txt") as t:
        for key in f:
            keys = key.rstrip("\n")
            for val in t:
                vals = val.rstrip("\n")
                raum[vals] = keys
raumrev = {value: key for (key, value) in raum.items()}

klass = {}
with open("data/klassenid.txt") as f:
    with open("data/klassen.txt") as t:
        for key in f:
            keys = key.rstrip("\n")
            for val in t:
                vals = val.rstrip("\n")
                klass[vals] = keys
klassrev = {value: key for (key, value) in klass.items()}

with open("data/neededrooms.txt") as i:
    for f in i:
        if f == 'stop':
            break
        istrip = f.rstrip("\n")
        for tt in s.timetable(start=mo, end=mo, room=raum.get(str(istrip))):
            print(tt.start)
            # if tt.start >= :
            #     print(raumrev.get(tt.kl))
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
