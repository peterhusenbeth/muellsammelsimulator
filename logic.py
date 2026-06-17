from data import LEVELS, punktzahlen_laden, punktzahlen_speichern


def gesamte_punktzahl_berechnen(punktzahlen):
    # Berechnet die Gesamtpunktzahl aus allen Level-Highscores
    return sum(punktzahlen.values())


def level_auswaehlen(level_id, punktzahlen):
    # Wird aufgerufen wenn ein Level-Knopf gedrückt wird
    level_name = LEVELS[level_id]["name"]
    print("Level " + str(level_id) + " ausgewaehlt: " + level_name)


def spiel_starten(level_id):
    # Gibt den Anfangszustand eines Levels zurück
    zustand = {}
    zustand["leben"] = 3
    zustand["punktzahl"] = 0
    zustand["level_id"] = level_id
    return zustand


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
    return ergebnis


def spiel_beendet(leben, verbleibend):
    # Prüft ob das Spiel vorbei ist
    if leben <= 0:
        return True
    if verbleibend <= 0:
        return True
    return False
