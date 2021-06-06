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
# print("Klasse", table.klassen, "hat in der", timetable.get(table.start), "in", table.rooms,
#       "unterricht.")

# Assign Class ID and Class Name to dictionary 'klass'
klass = {}
for f in s.klassen():
    raum[f.name] = f.id
klassrev = {key: value for (value, key) in raum.items()}

foo = [[], [], [], [], [], [], [], [], [], []]
klassen = foo[0]
zeit = foo[1]
raume = foo[2]
raumes1 = foo[3]
raumes2 = foo[4]
raumes3 = foo[5]
raumes4 = foo[6]
zeits1 = foo[7]
zeits2 = foo[8]
zeits3 = foo[9]
zeits4 = foo[10]


i = 0
ya = input("Welcher Wochentag? (Mo/Di)").lower()

with open("data/neededrooms.txt") as idx:
    for f in idx:
        istrip = f.rstrip("\n")
        ida = raum.get(istrip)

        if f == 'stop':
            break

        if ya == 'mo':
            for table in s.timetable(start=mo, end=mo, room=ida):
                klassen.append(table.klassen)
                zeit.append(timetable.get(table.start))
                raume.append(table.rooms)
                if table.start >= date(mo.year, mo.month, mo.day, 9, 55):
                    if check(str(raume[i])) == '[R1':
                        raumes1.append(raume[i])
                    elif check(str(raume[i])) == '[R2':
                        raumes2.append(raume[i])
                    elif check(str(raume[i])) == '[R3':
                        raumes3.append(raume[i])
                    else:
                        raumes4.append(raume[i])

                i += 1

            print('Im ersten Stock sind folgende Räume besetzt:\n')
            print('[%s]' % ', '.join(map(str, raumes1)))

            print('Im zweiten Stock sind folgende Räume besetzt:')
            print('[%s]' % ', '.join(map(str, raumes2)))

            print('Im dritten Stock sind folgende Räume besetzt:')
            print('[%s]' % ', '.join(map(str, raumes3)))

            print('Sontige Räume (Aula, Mensa etc) sind hier bestzt:')
            print('[%s]' % ', '.join(map(str, raumes4)))

        elif ya == 'di':
            for table in s.timetable(start=tu, end=tu, room=ida):
                klassen.append(table.klassen)
                zeit.append(timetable.get(table.start))
                raume.append(table.rooms)
                if table.start >= date(tu.year, tu.month, tu.day, 9, 55):
                    if check(str(raume[i])) == '[R1':
                        raumes1.append(raume[i])
                        zeits1.append(zeit[i])
                    elif check(str(raume[i])) == '[R2':
                        raumes2.append(raume[i])
                        zeits1.append(zeit[i])
                    elif check(str(raume[i])) == '[R3':
                        raumes3.append(raume[i])
                        zeits3.append(zeit[i])
                    else:
                        raumes4.append(raume[i])
                        zeits4.append(zeit[i])

                i += 1

            print('Im ersten Stock sind folgende Räume besetzt:\n')
            print('[%s]' % ', '.join(map(str, raumes1)), 'in der', ''.join(map(str, zeits1)))

            print('Im zweiten Stock sind folgende Räume besetzt:')
            print('[%s]' % ', '.join(map(str, raumes2)), 'in der', ''.join(map(str, zeits2)))

            print('Im dritten Stock sind folgende Räume besetzt:')
            print('[%s]' % ', '.join(map(str, raumes3)), 'in der', ''.join(map(str, zeits3)))

            print('Sontige Räume (Aula, Mensa etc) sind hier bestzt:')
            print('[%s]' % ', '.join(map(str, raumes4)), 'in der', ''.join(map(str, zeits4)))

        else:
            print("Kein gültiger Wochentag!")

s.logout()
