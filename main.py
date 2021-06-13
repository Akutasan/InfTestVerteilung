# main.py
import datetime
import os
import webuntis

from dotenv import load_dotenv

# LOGIN
load_dotenv()
NAME = os.getenv('NAME')
PASS = os.getenv('PASSKEY')

s = webuntis.Session(
    username=NAME,
    password=PASS,
    server='neilo.webuntis.com',
    school='Wilhelm-Raabe-Schule%20Lueneburg',
    useragent='WebUntis Test'
).login()

# DEFINE
today = datetime.date.today()
mo = today - datetime.timedelta(days=today.weekday())
tu = mo + datetime.timedelta(days=1)
date = datetime.datetime
zeit = []
raume = []
klassen = []
var = []
timetable = {
    "09:55:00": "3. Stunde",
    "10:45:00": "4. Stunde",
    "11:45:00": "5. Stunde",
    "12:35:00": "6. Stunde",
    "13:50:00": "7. Stunde",
    "14:35:00": "8. Stunde",
    "15:30:00": "9. Stunde",
    "16:15:00": "10. Stunde"
}

# Assign Room ID and Room Name to dictionary 'raum'
raum = {}
for f in s.rooms():
    raum[f.name] = f.id
raumrev = {key: value for (value, key) in raum.items()}

# Assign Class ID and Class Name to dictionary 'klass'
klass = {}
for f in s.klassen():
    raum[f.name] = f.id
klassrev = {key: value for (value, key) in raum.items()}


# Delete Duplicates of a list
def sort(getlist):
    seen = set()
    seen_add = seen.add
    return [x for x in getlist if not (x in seen or seen_add(x))]

# Ask variables
ya = input("Welcher Wochentag? (Mo/Di): ").lower()
ze = input("Welcher Zeitraum? (34/56): ").lower()

# MAIN

# Counter
i = 0

# Open neededrooms.txt
with open("data/neededrooms.txt") as idx:
    # Create enumerator
    for f in idx:
        istrip = f.rstrip("\n")
        ida = raum.get(istrip)

        # Check for keyword 'stop' in file
        if f == 'stop':
            break

        # Check for input monday (l. 61)
        if ya == 'mo':
            # Connect to table
            for table in s.timetable(start=mo, end=mo, room=ida):
                # Check if classes starts 9:55
                if table.start >= date(mo.year, mo.month, mo.day, 9, 55):
                    # Assign variables class, time, room and combination of latter two
                    klassen.append(table.klassen)
                    zeit.append(timetable.get(str(table.start)[-8:]))
                    raume.append(str(table.rooms))
                    var.append(zeit[i] + ': ' + raume[i])

                    # Check for input 34 or 56 (l. 62)
                    if ze == '34':
                        filtered_unsort = list(filter(lambda x: '3. Stunde' in x or '4. Stunde' in x, var))
                        filtered = sort(filtered_unsort)
                    elif ze == '56':
                        filtered_unsort = list(filter(lambda x: '5. Stunde' in x or '6. Stunde' in x, var))
                        filtered = sort(filtered_unsort)
                    else:
                        print("Kein gültiger Zeitraum!")
                        break

        # Check for input monday (l. 61)
        elif ya == 'di':
            # Connect to table
            for table in s.timetable(start=tu, end=tu, room=ida):
                # Check if classes starts 9:55
                if table.start >= date(tu.year, tu.month, tu.day, 9, 55):
                    # Assign variables class, time, room and combination of latter two
                    klassen.append(table.klassen)
                    zeit.append(timetable.get(str(table.start)[-8:]))
                    raume.append(str(table.rooms))
                    var.append(zeit[i] + ': ' + raume[i])

                    # Check for input 34 or 56 (l. 62)
                    if ze == '34':
                        filtered_unsort = list(filter(lambda x: '3. Stunde' in x or '4. Stunde' in x, var))
                        filtered = sort(filtered_unsort)
                    elif ze == '56':
                        filtered_unsort = list(filter(lambda x: '5. Stunde' in x or '6. Stunde' in x, var))
                        filtered = sort(filtered_unsort)
                    else:
                        print("Kein gültiger Zeitraum!")
                        break
        else:
            print("Kein gültiger Wochentag!")
            break

        # Count +1 to index counter
        i += 1
# LOUGOUT
s.logout()

# Seperation var
sep = ', '

# RESULT
# Check for storey and print list accordingly

dis = list(filter(lambda x: '[R0' in x, filtered))
dis.sort()
if not len(dis) == 0:
    print('Im erdgeschoss sind folgende Räume besetzt:')
    print(sep.join(dis))

dis = list(filter(lambda x: '[R1' in x, filtered))
dis.sort()
if not len(dis) == 0:
    print('Im ersten Stock sind folgende Räume besetzt:')
    print(sep.join(dis))

dis = list(filter(lambda x: '[R2' in x, filtered))
dis.sort()
if not len(dis) == 0:
    print('Im zweiten Stock sind folgende Räume besetzt:')
    print(sep.join(dis))

dis = list(filter(lambda x: '[R3' in x, filtered))
dis.sort()
if not len(dis) == 0:
    print('Im dritten Stock sind folgende Räume besetzt:')
    print(sep.join(dis))

dis = list(filter(lambda x: 'Aula' in x or 'Mensa' in x, filtered))
dis.sort()
if not len(dis) == 0:
    print('Sontige Räume (Aula, Mensa etc) sind hier bestzt:')
    print(sep.join(dis))
