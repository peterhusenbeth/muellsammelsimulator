import json
import os

# Level-Definitionen
LEVELS = {
    1: {"name": "Strand", "bild": "assets/level_01_strand.jpg"},
    2: {"name": "Wald", "bild": "assets/level_02_wald.jpg"},
    3: {"name": "Prärie", "bild": "assets/level_03_praerie.jpg"},
    4: {"name": "Feld", "bild": "assets/level_04_feld.jpg"},
    5: {"name": "Berg", "bild": "assets/level_05_berg.jpg"},
    6: {"name": "See", "bild": "assets/level_06_see.jpg"},
    7: {"name": "Wüste", "bild": "assets/level_07_wueste.jpg"},
    8: {"name": "Schnee", "bild": "assets/level_08_schnee.jpg"},
    9: {"name": "Dschungel", "bild": "assets/level_09_dschungel.jpg"},
    10: {"name": "Stadt", "bild": "assets/level_10_stadt.jpg"},
}

PUNKTZAHLEN_DATEI = "punktzahlen.json"


def standard_punktzahlen():
    # Gibt Punkte-Dict mit Null für alle Levels zurück
    punktzahlen = {}
    for level_id in LEVELS.keys():
        punktzahlen[level_id] = 0
    return punktzahlen


def punktzahlen_laden():
    # Lädt Punktzahlen aus JSON, gibt Dict mit Integer-Keys zurück
    if not os.path.exists(PUNKTZAHLEN_DATEI):
        return standard_punktzahlen()
    datei = open(PUNKTZAHLEN_DATEI, "r")
    geladene_daten = json.load(datei)
    datei.close()
    punktzahlen = {}
    for schluessel in geladene_daten.keys():
        punktzahlen[int(schluessel)] = geladene_daten[schluessel]
    return punktzahlen


def punktzahlen_speichern(punktzahlen):
    # Speichert Punktzahlen in JSON-Datei
    datei = open(PUNKTZAHLEN_DATEI, "w")
    json.dump(punktzahlen, datei, indent=2)
    datei.close()
