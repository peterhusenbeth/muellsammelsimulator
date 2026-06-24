import json
import os

# Level-Definitionen
LEVELS = {
    1: {"name": "Strand", "bild": "assets/level_01_strand.jpeg"},
    2: {"name": "Wald", "bild": "assets/level_02_wald.jpeg"},
    3: {"name": "Prärie", "bild": "assets/level_03_praerie.jpeg"},
    4: {"name": "Feld", "bild": "assets/level_04_feld.jpeg"},
    5: {"name": "Berg", "bild": "assets/level_05_berg.jpeg"},
    6: {"name": "See", "bild": "assets/level_06_see.jpeg"},
    7: {"name": "Wüste", "bild": "assets/level_07_wueste.jpeg"},
    8: {"name": "Schnee", "bild": "assets/level_08_schnee.jpeg"},
    9: {"name": "Dschungel", "bild": "assets/level_09_dschungel.jpeg"},
    10: {"name": "Stadt", "bild": "assets/level_10_stadt.jpeg"},
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
    11: [
        # Level 11 - Kanalisation (4 Müll + 4 Natur)
        {"name": "???", "typ": "muell", "bild": "assets/items/muell_???.png", "pos_x": 0.20, "pos_y": 0.30, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "muell", "bild": "assets/items/muell_???.png", "pos_x": 0.40, "pos_y": 0.35, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "muell", "bild": "assets/items/muell_???.png", "pos_x": 0.60, "pos_y": 0.30, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "muell", "bild": "assets/items/muell_???.png", "pos_x": 0.75, "pos_y": 0.35, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "natur", "bild": "assets/items/natur_???.png", "pos_x": 0.25, "pos_y": 0.50, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "natur", "bild": "assets/items/natur_???.png", "pos_x": 0.45, "pos_y": 0.55, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "natur", "bild": "assets/items/natur_???.png", "pos_x": 0.65, "pos_y": 0.50, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "natur", "bild": "assets/items/natur_???.png", "pos_x": 0.80, "pos_y": 0.55, "groesse": 1.0, "bewegung": None, "drehung": 0},
    ],
    12: [
        # Level 12 - Spielplatz (4 Müll + 4 Natur)
        {"name": "???", "typ": "muell", "bild": "assets/items/muell_???.png", "pos_x": 0.20, "pos_y": 0.30, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "muell", "bild": "assets/items/muell_???.png", "pos_x": 0.40, "pos_y": 0.35, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "muell", "bild": "assets/items/muell_???.png", "pos_x": 0.60, "pos_y": 0.30, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "muell", "bild": "assets/items/muell_???.png", "pos_x": 0.75, "pos_y": 0.35, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "natur", "bild": "assets/items/natur_???.png", "pos_x": 0.25, "pos_y": 0.50, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "natur", "bild": "assets/items/natur_???.png", "pos_x": 0.45, "pos_y": 0.55, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "natur", "bild": "assets/items/natur_???.png", "pos_x": 0.65, "pos_y": 0.50, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "natur", "bild": "assets/items/natur_???.png", "pos_x": 0.80, "pos_y": 0.55, "groesse": 1.0, "bewegung": None, "drehung": 0},
    ],
    13: [
        # Level 13 - ??? (4 Müll + 4 Natur)
        {"name": "???", "typ": "muell", "bild": "assets/items/muell_???.png", "pos_x": 0.20, "pos_y": 0.30, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "muell", "bild": "assets/items/muell_???.png", "pos_x": 0.40, "pos_y": 0.35, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "muell", "bild": "assets/items/muell_???.png", "pos_x": 0.60, "pos_y": 0.30, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "muell", "bild": "assets/items/muell_???.png", "pos_x": 0.75, "pos_y": 0.35, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "natur", "bild": "assets/items/natur_???.png", "pos_x": 0.25, "pos_y": 0.50, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "natur", "bild": "assets/items/natur_???.png", "pos_x": 0.45, "pos_y": 0.55, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "natur", "bild": "assets/items/natur_???.png", "pos_x": 0.65, "pos_y": 0.50, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "natur", "bild": "assets/items/natur_???.png", "pos_x": 0.80, "pos_y": 0.55, "groesse": 1.0, "bewegung": None, "drehung": 0},
    ],
    14: [
        # Level 14 - ??? (4 Müll + 4 Natur)
        {"name": "???", "typ": "muell", "bild": "assets/items/muell_???.png", "pos_x": 0.20, "pos_y": 0.30, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "muell", "bild": "assets/items/muell_???.png", "pos_x": 0.40, "pos_y": 0.35, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "muell", "bild": "assets/items/muell_???.png", "pos_x": 0.60, "pos_y": 0.30, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "muell", "bild": "assets/items/muell_???.png", "pos_x": 0.75, "pos_y": 0.35, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "natur", "bild": "assets/items/natur_???.png", "pos_x": 0.25, "pos_y": 0.50, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "natur", "bild": "assets/items/natur_???.png", "pos_x": 0.45, "pos_y": 0.55, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "natur", "bild": "assets/items/natur_???.png", "pos_x": 0.65, "pos_y": 0.50, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "natur", "bild": "assets/items/natur_???.png", "pos_x": 0.80, "pos_y": 0.55, "groesse": 1.0, "bewegung": None, "drehung": 0},
    ],
    15: [
        # Level 15 - ??? (4 Müll + 4 Natur)
        {"name": "???", "typ": "muell", "bild": "assets/items/muell_???.png", "pos_x": 0.20, "pos_y": 0.30, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "muell", "bild": "assets/items/muell_???.png", "pos_x": 0.40, "pos_y": 0.35, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "muell", "bild": "assets/items/muell_???.png", "pos_x": 0.60, "pos_y": 0.30, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "muell", "bild": "assets/items/muell_???.png", "pos_x": 0.75, "pos_y": 0.35, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "natur", "bild": "assets/items/natur_???.png", "pos_x": 0.25, "pos_y": 0.50, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "natur", "bild": "assets/items/natur_???.png", "pos_x": 0.45, "pos_y": 0.55, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "natur", "bild": "assets/items/natur_???.png", "pos_x": 0.65, "pos_y": 0.50, "groesse": 1.0, "bewegung": None, "drehung": 0},
        {"name": "???", "typ": "natur", "bild": "assets/items/natur_???.png", "pos_x": 0.80, "pos_y": 0.55, "groesse": 1.0, "bewegung": None, "drehung": 0},
    ],
}

# Kaufbare Levels (werden nach Kauf freigeschaltet)
KAUFBARE_LEVELS = {
    11: {"name": "Kanalisation", "bild": "assets/level_11_kanalisation.jpeg", "preis": 100},
    12: {"name": "Spielplatz", "bild": "assets/level_12_spielplatz.jpeg", "preis": 200},
    13: {"name": "???", "bild": "assets/level_13_unbekannt.jpeg", "preis": 300},
    14: {"name": "???", "bild": "assets/level_14_unbekannt.jpeg", "preis": 400},
    15: {"name": "???", "bild": "assets/level_15_unbekannt.jpeg", "preis": 500},
}

# Kaufbare Einzelgegenstände (erscheinen als Bonus-Item im Ziel-Level)
KAUFBARE_EINZEL_ITEMS = [
    {"name": "Schuh", "typ": "muell", "bild": "assets/items/muell_schuh.png", "preis": 20, "ziel_level": 6, "pos_x": 0.85, "pos_y": 0.25, "groesse": 0.9, "bewegung": None, "drehung": 15},
    {"name": "Fahrrad", "typ": "muell", "bild": "assets/items/muell_fahrrad.png", "preis": 30, "ziel_level": 1, "pos_x": 0.42, "pos_y": 0.12, "groesse": 2.0, "bewegung": None, "drehung": 0},
    {"name": "Bildschirm", "typ": "muell", "bild": "assets/items/muell_bildschirm.png", "preis": 40, "ziel_level": 10, "pos_x": 0.28, "pos_y": 0.12, "groesse": 1.1, "bewegung": None, "drehung": 350},
    {"name": "Tierschädel", "typ": "natur", "bild": "assets/items/natur_tierschaedel.png", "preis": 20, "ziel_level": 7, "pos_x": 0.20, "pos_y": 0.45, "groesse": 0.8, "bewegung": None, "drehung": 0},
    {"name": "Ananas", "typ": "natur", "bild": "assets/items/natur_ananas.png", "preis": 30, "ziel_level": 9, "pos_x": 0.38, "pos_y": 0.50, "groesse": 1.0, "bewegung": None, "drehung": 0},
    {"name": "Bienenstock", "typ": "natur", "bild": "assets/items/natur_bienenstock.png", "preis": 40, "ziel_level": 2, "pos_x": 0.40, "pos_y": 0.55, "groesse": 1.1, "bewegung": None, "drehung": 0},
]

# Alles Kaufbare zusammengefasst
KAUFBARE_GEGENSTAENDE = {
    "levels": KAUFBARE_LEVELS,
    "items": KAUFBARE_EINZEL_ITEMS,
}

PUNKTZAHLEN_DATEI = "punktzahlen.json"


def standard_punktzahlen():
    # Gibt Punkte-Dict mit Null für alle Levels zurück
    punktzahlen = {}
    for level_id in LEVELS.keys():
        punktzahlen[level_id] = 0
    return punktzahlen


def alle_daten_laden():
    # Lädt die ganze Speicherdatei (Punkte, Zeiten und Einkäufe)
    if not os.path.exists(PUNKTZAHLEN_DATEI):
        return {"punktzahlen": {}, "zeiten": {}, "einkaeufe": {"levels": [], "items": []}}
    datei = open(PUNKTZAHLEN_DATEI, "r")
    inhalt = json.load(datei)
    datei.close()
    # Alte Dateien hatten nur die Punkte direkt drin
    if "punktzahlen" not in inhalt:
        return {"punktzahlen": inhalt, "zeiten": {}, "einkaeufe": {"levels": [], "items": []}}
    if "einkaeufe" not in inhalt:
        inhalt["einkaeufe"] = {"levels": [], "items": []}
    return inhalt


def alle_daten_speichern(daten):
    # Schreibt die ganze Speicherdatei (Punkte und Zeiten)
    datei = open(PUNKTZAHLEN_DATEI, "w")
    json.dump(daten, datei, indent=2)
    datei.close()


def werte_pro_level_laden(schluessel):
    # Lädt einen Teil (z.B. "punktzahlen" oder "zeiten") mit Zahlen-Keys
    daten = alle_daten_laden()
    rohe_werte = daten.get(schluessel, {})
    alle_levels = aktive_levels_holen()
    werte = {}
    for level_id in alle_levels.keys():
        werte[level_id] = rohe_werte.get(str(level_id), 0)
    return werte


def punktzahlen_laden():
    # Lädt die Punktzahlen, gibt Dict mit Integer-Keys zurück
    return werte_pro_level_laden("punktzahlen")


def zeiten_laden():
    # Lädt die Zeiten (in Millisekunden), gibt Dict mit Integer-Keys zurück
    return werte_pro_level_laden("zeiten")


def punktzahlen_speichern(punktzahlen):
    # Speichert die Punktzahlen, die Zeiten bleiben erhalten
    daten = alle_daten_laden()
    daten["punktzahlen"] = punktzahlen
    alle_daten_speichern(daten)


def zeiten_speichern(zeiten):
    # Speichert die Zeiten, die Punktzahlen bleiben erhalten
    daten = alle_daten_laden()
    daten["zeiten"] = zeiten
    alle_daten_speichern(daten)


def beste_punktzahl_aktualisieren(level_id, neue_punktzahl):
    # Speichert die Punktzahl wenn sie besser als die bisherige ist
    punktzahlen = punktzahlen_laden()
    alte_punktzahl = punktzahlen.get(level_id, 0)
    if neue_punktzahl > alte_punktzahl:
        punktzahlen[level_id] = neue_punktzahl
        punktzahlen_speichern(punktzahlen)
        return True
    return False


def beste_zeit_aktualisieren(level_id, neue_zeit):
    # Speichert die Zeit wenn sie besser (kleiner) als die bisherige ist
    zeiten = zeiten_laden()
    alte_zeit = zeiten.get(level_id, 0)
    if alte_zeit == 0 or neue_zeit < alte_zeit:
        zeiten[level_id] = neue_zeit
        zeiten_speichern(zeiten)
        return True
    return False


def einkaeufe_laden():
    # Lädt die Einkäufe aus der Speicherdatei
    daten = alle_daten_laden()
    return daten.get("einkaeufe", {"levels": [], "items": []})


def einkaeufe_speichern(einkaeufe):
    # Speichert die Einkäufe in die Speicherdatei
    daten = alle_daten_laden()
    daten["einkaeufe"] = einkaeufe
    alle_daten_speichern(daten)


def einkauf_durchfuehren(name, kategorie):
    # Fügt einen Kauf hinzu (kategorie ist "levels" oder "items")
    einkaeufe = einkaeufe_laden()
    if name not in einkaeufe[kategorie]:
        einkaeufe[kategorie].append(name)
        einkaeufe_speichern(einkaeufe)


def ist_gekauft(name, einkaeufe):
    # Prüft ob ein Level oder Item schon gekauft wurde
    if name in einkaeufe["levels"]:
        return True
    if name in einkaeufe["items"]:
        return True
    return False


def aktive_levels_holen():
    # Gibt alle spielbaren Levels zurück (Basis + gekaufte)
    ergebnis = {}
    for level_id in LEVELS:
        ergebnis[level_id] = LEVELS[level_id]
    einkaeufe = einkaeufe_laden()
    for level_id in KAUFBARE_LEVELS:
        if level_id in einkaeufe["levels"]:
            ergebnis[level_id] = KAUFBARE_LEVELS[level_id]
    return ergebnis


def aktive_gegenstaende_holen(level_id):
    # Gibt Gegenstände für ein Level zurück, inklusive gekaufter Bonus-Items
    basis = []
    if level_id in GEGENSTAENDE:
        for item in GEGENSTAENDE[level_id]:
            basis.append(item)
    einkaeufe = einkaeufe_laden()
    for item in KAUFBARE_EINZEL_ITEMS:
        if item["ziel_level"] == level_id and item["name"] in einkaeufe["items"]:
            basis.append(item)
    return basis


def guthaben_berechnen(punktzahlen, einkaeufe):
    # Berechnet das Guthaben (Gesamtpunktzahl minus Ausgaben)
    gesamt = 0
    for punkte in punktzahlen.values():
        gesamt = gesamt + punkte
    ausgaben = 0
    for level_id in einkaeufe["levels"]:
        if level_id in KAUFBARE_LEVELS:
            ausgaben = ausgaben + KAUFBARE_LEVELS[level_id]["preis"]
    for item_name in einkaeufe["items"]:
        for item in KAUFBARE_EINZEL_ITEMS:
            if item["name"] == item_name:
                ausgaben = ausgaben + item["preis"]
    return gesamt - ausgaben
