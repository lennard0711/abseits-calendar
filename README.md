# abseits-calendar
Mit diesem Projekt lassen sich die Ansetzungen von https://abseits.biz in einen Webkalender via CalDav importieren.

## Benötigte Environment Variablen
### ABSEITS_KADER
> :warning: **Die Variable muss dem aktuellen Kader, unter dem der Schiedsrichter auf abseits.biz zu finden ist, entsprechen**

Die Variable `ABSEITS_KADER` kann folgende Werte haben:
| Kader | Wert |
| ----- | ---- |
| Amateurliga | Amat |
| Bezirksliga | BZL |
| NLK-I | NLK-I |
| NLK-II | NLK-II |
| Sichtungsgruppe | SG |
| Assistenten | SRA |

### ABSEITS_UID
Die eigene `ABSEITS_UID` kann wie folgt herausgefunden werden:
1. Man öffnet https://abeits.biz
2. Unter `Spiele` wählt man den eigenen Kader aus
3. Rechtsklick auf den eigenen Namen
4. Link in neuem Tab öffnen
5. Nun öffnet sich abseits.biz in einem neuen Tab mit einer URL die ungefähr so aussieht `https://abseits.biz/php/index.php?pagename=Steckbrief&startpage=srdaten%2Fsrdaten.php%3Fid%3D400000000205`
6. Alle zusammenhängende Ziffern am Ende der URL sind die UID des Benutzers
7. In diesem Beispiel wäre die UID nun `400000000205`

### ABSEITS_USER
> :exclamation: **Diese Variable wird genutzt um sich auf abseits.biz einzuloggen, damit auch nicht-öffentliche Einträge in den Kalender importiert werden können!**

Die Variable `ABSEITS_USER` entspricht des eigenen Nutzernamens von abseits.biz.

### ABSEITS_PASSWORD
> :exclamation: **Diese Variable wird genutzt um sich auf abseits.biz einzuloggen, damit auch nicht-öffentliche Einträge in den Kalender importiert werden können!**

Die Variable `ABSEITS_PASSWORD` entspricht des zugehörigen Passworts des Nutzers von abseits.biz.

### CALDAV_URL
Die Variable `CALDAV_URL` muss auf einen validen CalDav Endpoint zeigen z.B. `https://nextcloud.example.com/remote.php/dav`.

### CALDAV_USER
Die Variable `CALDAV_USER` enthält den Nutzernamen der für den Login am CalDav Endpoint nötig ist.

### CALDAV_PASSWORD
Die Variable `CALDAV_PASSWORD` enthält das zugehörige Passwort zum `CALDAV_USER`

### CALDAV_CALENDAR
In der Variable `CALDAV_CALENDAR` wird der Name des zu nutzenden Kalenders festgelegt.

Wenn der Kalender nicht existiert, wird dieser erstellt.

Der Defaultwert lautet `Abseits`