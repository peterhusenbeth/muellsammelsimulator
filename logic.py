import time
from data import aktive_levels_holen, aktive_gegenstaende_holen
from data import beste_punktzahl_aktualisieren, beste_zeit_aktualisieren

# Spielzustand — logic schreibt, main liest
zustand = {}



###### Menü-Logik ######
def gesamte_punktzahl_berechnen(punktzahlen):
    # Berechnet die Gesamtpunktzahl aus allen Level-Highscores
    return sum(punktzahlen.values())


def gesamte_zeit_berechnen(zeiten):
    # Addiert alle Levelzeiten zusammen (in Millisekunden)
    return sum(zeiten.values())


def abgeschlossene_level_zaehlen(zeiten):
    # Zählt wie viele Level schon geschafft wurden (Zeit groesser als 0)
    anzahl = 0
    for zeit in zeiten.values():
        if zeit > 0:
            anzahl = anzahl + 1
    return anzahl


def level_auswaehlen(level_id, punktzahlen):
    # Wird aufgerufen wenn ein Level-Knopf gedrückt wird
    alle_levels = aktive_levels_holen()
    level_name = alle_levels[level_id]["name"]
    print("Level " + str(level_id) + " ausgewaehlt: " + level_name)



###### Spiel-Logik ######
def spiel_starten(level_id):
    # Setzt den Spielzustand auf Anfangswerte zurück
    zustand["level_id"] = level_id
    zustand["leben"] = 3
    zustand["punktzahl"] = 0
    zustand["start_zeit"] = 0.0
    zustand["laufende_zeit"] = 0.0
    zustand["anzahl_verbleibend"] = len(aktive_gegenstaende_holen(level_id))
    zustand["beendet"] = False
    zustand["gewonnen"] = False


def timer_starten():
    # Setzt die Startzeit auf jetzt
    zustand["start_zeit"] = time.monotonic()
    zustand["laufende_zeit"] = 0.0


def timer_aktualisieren():
    # Berechnet die vergangene Zeit seit dem Start
    zustand["laufende_zeit"] = time.monotonic() - zustand["start_zeit"]


def ecke_erkennen(rel_x, rel_y):
    # Erkennt ob eine Position in einer Ecke liegt
    if rel_y < 0.25:
        if rel_x < 0.25:
            return "natur_ecke"
        if rel_x > 0.75:
            return "muell_ecke"
    return "keine"


def gegenstand_pruefen(gegenstand_typ, ziel_ecke):
    # Prüft ob ein Gegenstand richtig zugeordnet wurde
    ergebnis = {}
    ergebnis["richtig"] = False
    ergebnis["punkte"] = 0
    ergebnis["leben"] = 0
    if gegenstand_typ == "muell" and ziel_ecke == "muell_ecke":
        ergebnis["richtig"] = True
        ergebnis["punkte"] = 10
    if gegenstand_typ == "natur" and ziel_ecke == "natur_ecke":
        ergebnis["richtig"] = True
        ergebnis["punkte"] = 5
    if not ergebnis["richtig"]:
        ergebnis["leben"] = -1
        ergebnis["punkte"] = -2
    return ergebnis


def gegenstand_ablegen(gegenstand_typ, rel_x, rel_y):
    # Verarbeitet das Ablegen eines Gegenstands und aktualisiert den Zustand
    ecke = ecke_erkennen(rel_x, rel_y)
    if ecke == "keine":
        return {"richtig": False, "ecke": "keine"}
    pruefung = gegenstand_pruefen(gegenstand_typ, ecke)
    zustand["punktzahl"] = zustand["punktzahl"] + pruefung["punkte"]
    if zustand["punktzahl"] < 0:
        zustand["punktzahl"] = 0
    zustand["leben"] = zustand["leben"] + pruefung["leben"]
    if pruefung["richtig"]:
        zustand["anzahl_verbleibend"] = zustand["anzahl_verbleibend"] - 1
    ende_pruefen()
    return {"richtig": pruefung["richtig"], "ecke": ecke}


def ende_pruefen():
    # Setzt die Flags wenn das Spiel vorbei ist
    if zustand["leben"] <= 0:
        zustand["beendet"] = True
        zustand["gewonnen"] = False
    if zustand["anzahl_verbleibend"] <= 0:
        zustand["beendet"] = True
        zustand["gewonnen"] = True

def zeit_bewerten():
    if zustand["gewonnen"] and zustand["laufende_zeit"] < 10.0:
        zustand["punktzahl"] = zustand["punktzahl"] + 50

def ergebnis_speichern():
    # Speichert Punktzahl und (bei Sieg) die Zeit
    level_id = zustand["level_id"]
    beste_punktzahl_aktualisieren(level_id, zustand["punktzahl"])
    if zustand["gewonnen"]:
        zeit_ms = int(zustand["laufende_zeit"] * 1000)
        beste_zeit_aktualisieren(level_id, zeit_ms)
