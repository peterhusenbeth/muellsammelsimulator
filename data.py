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

# Gegenstände pro Level (je 8 Stück, 4 Müll + 4 Natur)
# Positionen logisch: Vögel oben, Bäume mitte-oben, Tiere mitte, Müll unten
# "groesse": Größenfaktor (1.0 = normal). "bewegung": None, "kreisen", "schwingen" oder "huepfen"
# "drehung": Drehwinkel in Grad (0 = gerade, z.B. 45 = schräg nach links gekippt)
GEGENSTAENDE = {
    1: [
        {"name": "Flasche", "typ": "muell", "bild": "assets/items/muell_flasche.png", "pos_x": 0.32, "pos_y": 0.15, "groesse": 1.5, "bewegung": None, "drehung": 340},
        {"name": "Tüte", "typ": "muell", "bild": "assets/items/muell_tuete.png", "pos_x": 0.85, "pos_y": 0.50, "groesse": 0.8, "bewegung": "kreisen", "drehung": 12},
        {"name": "Dose", "typ": "muell", "bild": "assets/items/muell_dose.png", "pos_x": 0.67, "pos_y": 0.15, "groesse": 1.0, "bewegung": None, "drehung": 270},
        {"name": "Becher", "typ": "muell", "bild": "assets/items/muell_becher.png", "pos_x": 0.23, "pos_y": 0.33, "groesse": 0.4, "bewegung": None, "drehung": 80},
        {"name": "Muschel", "typ": "natur", "bild": "assets/items/natur_muschel.png", "pos_x": 0.45, "pos_y": 0.27, "groesse": 0.5, "bewegung": None, "drehung": 0},
        {"name": "Krabbe", "typ": "natur", "bild": "assets/items/natur_krabbe.png", "pos_x": 0.11, "pos_y": 0.28, "groesse": 0.8, "bewegung": "huepfen", "drehung": 0},
        {"name": "Seestern", "typ": "natur", "bild": "assets/items/natur_seestern.png", "pos_x": 0.75, "pos_y": 0.27, "groesse": 1.3, "bewegung": None, "drehung": 0},
        {"name": "Alge", "typ": "natur", "bild": "assets/items/natur_alge.png", "pos_x": 0.33, "pos_y": 0.50, "groesse": 0.7, "bewegung": "schwingen", "drehung": 0},
    ],
    2: [
        {"name": "Zeitung", "typ": "muell", "bild": "assets/items/muell_zeitung.png", "pos_x": 0.60, "pos_y": 0.02, "groesse": 1.7, "bewegung": None, "drehung": 340},
        {"name": "Batterie", "typ": "muell", "bild": "assets/items/muell_batterie.png", "pos_x": 0.02, "pos_y": 0.26, "groesse": 0.4, "bewegung": None, "drehung": 89},
        {"name": "Dose", "typ": "muell", "bild": "assets/items/muell_dose.png", "pos_x": 0.47, "pos_y": 0.24, "groesse": 0.3, "bewegung": None, "drehung": 87},
        {"name": "Karton", "typ": "muell", "bild": "assets/items/muell_karton.png", "pos_x": 0.78, "pos_y": 0.32, "groesse": 0.9, "bewegung": None, "drehung": 355},
        {"name": "Pilz", "typ": "natur", "bild": "assets/items/natur_pilz.png", "pos_x": 0.33, "pos_y": 0.17, "groesse": 0.6, "bewegung": None, "drehung": 0},
        {"name": "Eichel", "typ": "natur", "bild": "assets/items/natur_eichel.png", "pos_x": 0.41, "pos_y": 0.07, "groesse": 1.1, "bewegung": None, "drehung": 34},
        {"name": "Igel", "typ": "natur", "bild": "assets/items/natur_igel.png", "pos_x": 0.165, "pos_y": 0.28, "groesse": 1.0, "bewegung": "huepfen", "drehung": 0},
        {"name": "Blatt", "typ": "natur", "bild": "assets/items/natur_blatt.png", "pos_x": 0.62, "pos_y": 0.68, "groesse": 0.8, "bewegung": "schwingen", "drehung": 256},
    ],
    3: [
        {"name": "Flasche", "typ": "muell", "bild": "assets/items/muell_flasche.png", "pos_x": 0.40, "pos_y": 0.32, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Tüte", "typ": "muell", "bild": "assets/items/muell_tuete.png", "pos_x": 0.20, "pos_y": 0.50, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Kippe", "typ": "muell", "bild": "assets/items/muell_kippe.png", "pos_x": 0.60, "pos_y": 0.30, "groesse": 0.6, "bewegung": None, "drehung": 0},
        {"name": "Becher", "typ": "muell", "bild": "assets/items/muell_becher.png", "pos_x": 0.75, "pos_y": 0.35, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Blume", "typ": "natur", "bild": "assets/items/natur_blume.png", "pos_x": 0.30, "pos_y": 0.42, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Schmetterling", "typ": "natur", "bild": "assets/items/natur_schmetterling.png", "pos_x": 0.50, "pos_y": 0.65, "groesse": 1.0, "bewegung": "schwingen", "drehung": 0},
        {"name": "Weizen", "typ": "natur", "bild": "assets/items/natur_weizen.png", "pos_x": 0.15, "pos_y": 0.50, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Vogel", "typ": "natur", "bild": "assets/items/natur_vogel.png", "pos_x": 0.70, "pos_y": 0.68, "groesse": 1.0, "bewegung": "kreisen", "drehung": 0},
    ],
    4: [
        {"name": "Dose", "typ": "muell", "bild": "assets/items/muell_dose.png", "pos_x": 0.35, "pos_y": 0.30, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Zeitung", "typ": "muell", "bild": "assets/items/muell_zeitung.png", "pos_x": 0.15, "pos_y": 0.33, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Karton", "typ": "muell", "bild": "assets/items/muell_karton.png", "pos_x": 0.55, "pos_y": 0.28, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Batterie", "typ": "muell", "bild": "assets/items/muell_batterie.png", "pos_x": 0.70, "pos_y": 0.32, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Käfer", "typ": "natur", "bild": "assets/items/natur_kaefer.png", "pos_x": 0.25, "pos_y": 0.38, "groesse": 0.7, "bewegung": "huepfen", "drehung": 0},
        {"name": "Raupe", "typ": "natur", "bild": "assets/items/natur_raupe.png", "pos_x": 0.60, "pos_y": 0.40, "groesse": 0.7, "bewegung": "huepfen", "drehung": 0},
        {"name": "Maus", "typ": "natur", "bild": "assets/items/natur_maus.png", "pos_x": 0.45, "pos_y": 0.42, "groesse": 1.0, "bewegung": "huepfen", "drehung": 0},
        {"name": "Sonnenblume", "typ": "natur", "bild": "assets/items/natur_sonnenblume.png", "pos_x": 0.75, "pos_y": 0.55, "groesse": 1.2, "bewegung": None, "drehung": 0},
    ],
    5: [
        {"name": "Flasche", "typ": "muell", "bild": "assets/items/muell_flasche.png", "pos_x": 0.30, "pos_y": 0.35, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Tüte", "typ": "muell", "bild": "assets/items/muell_tuete.png", "pos_x": 0.50, "pos_y": 0.52, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Becher", "typ": "muell", "bild": "assets/items/muell_becher.png", "pos_x": 0.15, "pos_y": 0.32, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Dose", "typ": "muell", "bild": "assets/items/muell_dose.png", "pos_x": 0.65, "pos_y": 0.30, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Adler", "typ": "natur", "bild": "assets/items/natur_adler.png", "pos_x": 0.40, "pos_y": 0.70, "groesse": 1.3, "bewegung": "kreisen", "drehung": 0},
        {"name": "Blume", "typ": "natur", "bild": "assets/items/natur_blume.png", "pos_x": 0.20, "pos_y": 0.42, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Schmetterling", "typ": "natur", "bild": "assets/items/natur_schmetterling.png", "pos_x": 0.60, "pos_y": 0.62, "groesse": 1.0, "bewegung": "schwingen", "drehung": 0},
        {"name": "Ziege", "typ": "natur", "bild": "assets/items/natur_ziege.png", "pos_x": 0.75, "pos_y": 0.45, "groesse": 1.2, "bewegung": "huepfen", "drehung": 0},
    ],
    6: [
        {"name": "Dose", "typ": "muell", "bild": "assets/items/muell_dose.png", "pos_x": 0.35, "pos_y": 0.32, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Flasche", "typ": "muell", "bild": "assets/items/muell_flasche.png", "pos_x": 0.15, "pos_y": 0.35, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Becher", "typ": "muell", "bild": "assets/items/muell_becher.png", "pos_x": 0.60, "pos_y": 0.30, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Tüte", "typ": "muell", "bild": "assets/items/muell_tuete.png", "pos_x": 0.50, "pos_y": 0.48, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Frosch", "typ": "natur", "bild": "assets/items/natur_frosch.png", "pos_x": 0.25, "pos_y": 0.38, "groesse": 1.0, "bewegung": "huepfen", "drehung": 0},
        {"name": "Ente", "typ": "muell", "bild": "assets/items/muell_ente.png", "pos_x": 0.45, "pos_y": 0.40, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Fisch", "typ": "natur", "bild": "assets/items/natur_fisch.png", "pos_x": 0.70, "pos_y": 0.33, "groesse": 1.0, "bewegung": "schwingen", "drehung": 0},
        {"name": "Libelle", "typ": "natur", "bild": "assets/items/natur_libelle.png", "pos_x": 0.55, "pos_y": 0.65, "groesse": 1.0, "bewegung": "kreisen", "drehung": 0},
    ],
    7: [
        {"name": "Dose", "typ": "muell", "bild": "assets/items/muell_dose.png", "pos_x": 0.20, "pos_y": 0.32, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Batterie", "typ": "muell", "bild": "assets/items/muell_batterie.png", "pos_x": 0.55, "pos_y": 0.30, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Zeitung", "typ": "muell", "bild": "assets/items/muell_zeitung.png", "pos_x": 0.40, "pos_y": 0.35, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Karton", "typ": "muell", "bild": "assets/items/muell_karton.png", "pos_x": 0.70, "pos_y": 0.28, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Kaktus", "typ": "natur", "bild": "assets/items/natur_kaktus.png", "pos_x": 0.30, "pos_y": 0.52, "groesse": 1.2, "bewegung": None, "drehung": 0},
        {"name": "Skorpion", "typ": "natur", "bild": "assets/items/natur_skorpion.png", "pos_x": 0.60, "pos_y": 0.38, "groesse": 1.0, "bewegung": "huepfen", "drehung": 0},
        {"name": "Schlange", "typ": "natur", "bild": "assets/items/natur_schlange.png", "pos_x": 0.15, "pos_y": 0.40, "groesse": 1.2, "bewegung": "huepfen", "drehung": 0},
    ],
    8: [
        {"name": "Flasche", "typ": "muell", "bild": "assets/items/muell_flasche.png", "pos_x": 0.35, "pos_y": 0.33, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Becher", "typ": "muell", "bild": "assets/items/muell_becher.png", "pos_x": 0.15, "pos_y": 0.30, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Tüte", "typ": "muell", "bild": "assets/items/muell_tuete.png", "pos_x": 0.55, "pos_y": 0.50, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Dose", "typ": "muell", "bild": "assets/items/muell_dose.png", "pos_x": 0.65, "pos_y": 0.32, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Hase", "typ": "natur", "bild": "assets/items/natur_hase.png", "pos_x": 0.25, "pos_y": 0.40, "groesse": 1.0, "bewegung": "huepfen", "drehung": 0},
        {"name": "Eule", "typ": "natur", "bild": "assets/items/natur_eule.png", "pos_x": 0.45, "pos_y": 0.62, "groesse": 1.0, "bewegung": "kreisen", "drehung": 0},
        {"name": "Schneeflocke", "typ": "natur", "bild": "assets/items/natur_schneeflocke.png", "pos_x": 0.70, "pos_y": 0.68, "groesse": 0.8, "bewegung": "schwingen", "drehung": 0},
        {"name": "Tanne", "typ": "natur", "bild": "assets/items/natur_tanne.png", "pos_x": 0.20, "pos_y": 0.55, "groesse": 1.3, "bewegung": None, "drehung": 0},
    ],
    9: [
        {"name": "Dose", "typ": "muell", "bild": "assets/items/muell_dose.png", "pos_x": 0.30, "pos_y": 0.30, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Batterie", "typ": "muell", "bild": "assets/items/muell_batterie.png", "pos_x": 0.60, "pos_y": 0.32, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Zeitung", "typ": "muell", "bild": "assets/items/muell_zeitung.png", "pos_x": 0.15, "pos_y": 0.35, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Flasche", "typ": "muell", "bild": "assets/items/muell_flasche.png", "pos_x": 0.45, "pos_y": 0.28, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Papagei", "typ": "natur", "bild": "assets/items/natur_papagei.png", "pos_x": 0.50, "pos_y": 0.68, "groesse": 1.0, "bewegung": "kreisen", "drehung": 0},
        {"name": "Affe", "typ": "natur", "bild": "assets/items/natur_affe.png", "pos_x": 0.35, "pos_y": 0.58, "groesse": 1.2, "bewegung": "huepfen", "drehung": 0},
        {"name": "Schlange", "typ": "natur", "bild": "assets/items/natur_schlange.png", "pos_x": 0.70, "pos_y": 0.40, "groesse": 1.2, "bewegung": "huepfen", "drehung": 0},
        {"name": "Blume", "typ": "natur", "bild": "assets/items/natur_blume.png", "pos_x": 0.20, "pos_y": 0.45, "groesse": 1.0, "bewegung": None, "drehung": 0},
    ],
    10: [
        {"name": "Zeitung", "typ": "muell", "bild": "assets/items/muell_zeitung.png", "pos_x": 0.40, "pos_y": 0.32, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Dose", "typ": "muell", "bild": "assets/items/muell_dose.png", "pos_x": 0.15, "pos_y": 0.30, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Becher", "typ": "muell", "bild": "assets/items/muell_becher.png", "pos_x": 0.60, "pos_y": 0.33, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Karton", "typ": "muell", "bild": "assets/items/muell_karton.png", "pos_x": 0.30, "pos_y": 0.28, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "Taube", "typ": "natur", "bild": "assets/items/natur_taube.png", "pos_x": 0.50, "pos_y": 0.65, "groesse": 1.0, "bewegung": "kreisen", "drehung": 0},
        {"name": "Eichhörnchen", "typ": "natur", "bild": "assets/items/natur_eichhoernchen.png", "pos_x": 0.70, "pos_y": 0.55, "groesse": 1.0, "bewegung": "huepfen", "drehung": 0},
        {"name": "Baum", "typ": "natur", "bild": "assets/items/natur_baum.png", "pos_x": 0.25, "pos_y": 0.52, "groesse": 1.4, "bewegung": None, "drehung": 0},
        {"name": "Blume", "typ": "natur", "bild": "assets/items/natur_blume.png", "pos_x": 0.75, "pos_y": 0.42, "groesse": 1.0, "bewegung": None, "drehung": 0},
    ],
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


def beste_punktzahl_aktualisieren(level_id, neue_punktzahl):
    # Speichert die Punktzahl wenn sie besser als die bisherige ist
    punktzahlen = punktzahlen_laden()
    alte_punktzahl = punktzahlen.get(level_id, 0)
    if neue_punktzahl > alte_punktzahl:
        punktzahlen[level_id] = neue_punktzahl
        punktzahlen_speichern(punktzahlen)
        return True
    return False
