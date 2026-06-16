from data import LEVELS, punktzahlen_laden, punktzahlen_speichern


def gesamte_punktzahl_berechnen(punktzahlen):
    # Berechnet die Gesamtpunktzahl aus allen Level-Highscores
    return sum(punktzahlen.values())


def level_auswaehlen(level_id, punktzahlen):
    # Wird aufgerufen wenn ein Level-Knopf gedrückt wird
    level_name = LEVELS[level_id]["name"]
    print("Level " + str(level_id) + " ausgewaehlt: " + level_name)
