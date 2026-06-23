import sys
import math
from kivy.config import Config
if sys.platform == "linux":
    Config.set("graphics", "fullscreen", "auto")
else:
    Config.set("graphics", "position", "custom")
    Config.set("graphics", "left", 630)
    Config.set("graphics", "top", 1441)
    Config.set("graphics", "fullscreen", "auto")

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.utils import platform
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from data import LEVELS, punktzahlen_laden, zeiten_laden
from data import KAUFBARE_LEVELS, KAUFBARE_EINZEL_ITEMS
from data import einkaeufe_laden, einkauf_durchfuehren, ist_gekauft
from data import aktive_levels_holen, aktive_gegenstaende_holen, guthaben_berechnen
import logic
from logic import gesamte_punktzahl_berechnen, level_auswaehlen
from logic import gesamte_zeit_berechnen, abgeschlossene_level_zaehlen

DESIGN_BREITE = 2000
DESIGN_HOEHE = 1200
BASIS_GROESSE = 100

###### Hilfsfunktionen ######


def zeit_text(millisekunden):
    # Wandelt Millisekunden in den Text MM:SS:mmm um
    ganze_sekunden = millisekunden // 1000
    minuten = ganze_sekunden // 60
    rest_sekunden = ganze_sekunden % 60
    millis = millisekunden % 1000
    muster = "{0:02d}:{1:02d}:{2:03d}"
    return muster.format(minuten, rest_sekunden, millis)


def abdunkel_animation(widget):
    # Dunkelt den Button kurz ab als Klick-Feedback
    r = float(widget.background_color[0])
    g = float(widget.background_color[1])
    b = float(widget.background_color[2])
    a = float(widget.background_color[3])
    if a < 0.1:
        a = 0.3
    dunkel = [r * 0.6, g * 0.6, b * 0.6, a]
    original = [r, g, b, float(widget.background_color[3])]
    anim = Animation(background_color=dunkel, duration=0.08)
    anim = anim + Animation(background_color=original, duration=0.08)
    anim.start(widget)



###### Widget-Klassen ######

class LevelContainer(FloatLayout):
    pass


class LevelContainerBonus(FloatLayout):
    pass


class ScoreBox(BoxLayout):
    pass


class ScoreBoxBonus(BoxLayout):
    pass



class ShopArtikel(FloatLayout):
    pass


class ErgebnisOverlay(FloatLayout):
    pass


class SirenenLicht(Widget):
    pass


class GegenstandWidget(Image):
    # Drehwinkel in Grad, wird im spiel.kv zum Drehen des Bildes benutzt
    drehung = NumericProperty(0)

    def __init__(self):
        super().__init__()
        self.gegenstand_typ = ""
        self.gegenstand_name = ""
        self.start_x = 0
        self.start_y = 0
        self.bewegung = None


###### Menü-Bildschirm ######

class MenuBildschirm(Screen):
    def __init__(self):
        super().__init__()
        self.punktzahlen = punktzahlen_laden()
        self.zeiten = zeiten_laden()
        self.gewaehltes_level = None
        Clock.schedule_once(self.ui_aufbauen, 0)

    def ui_aufbauen(self, _dt):
        # Baut die Menü-Oberfläche auf
        self.level_buttons_erstellen()
        self.gesamtpunktzahl_aktualisieren()

    def level_buttons_erstellen(self):
        # Erstellt alle Level-Buttons und verteilt sie auf die Spalten
        left_col = self.ids.left_column
        right_col = self.ids.right_column
        left_col.clear_widgets()
        right_col.clear_widgets()
        zaehler = 0
        for level_id in sorted(LEVELS.keys()):
            level_data = LEVELS[level_id]
            score = self.punktzahlen.get(level_id, 0)
            zeit = self.zeiten.get(level_id, 0)
            button = self.level_button_erstellen(level_id, level_data["name"], score, zeit)
            if zaehler < 5:
                left_col.add_widget(button)
            else:
                right_col.add_widget(button)
            zaehler = zaehler + 1
        self.bonus_levels_erstellen()

    def bonus_levels_erstellen(self):
        # Zeigt gekaufte Bonus-Levels in zwei Spalten an
        left = self.ids.bonus_left
        right = self.ids.bonus_right
        left.clear_widgets()
        right.clear_widgets()
        einkaeufe = einkaeufe_laden()
        zaehler = 0
        for level_id in sorted(KAUFBARE_LEVELS.keys()):
            if level_id not in einkaeufe["levels"]:
                continue
            level_data = KAUFBARE_LEVELS[level_id]
            score = self.punktzahlen.get(level_id, 0)
            zeit = self.zeiten.get(level_id, 0)
            button = self.bonus_button_erstellen(level_id, level_data["name"], score, zeit)
            if zaehler % 2 == 0:
                left.add_widget(button)
            else:
                right.add_widget(button)
            zaehler = zaehler + 1
        self.bonus_container_groesse_anpassen(zaehler)

    def bonus_container_groesse_anpassen(self, anzahl):
        # Passt die Höhe des Bonus-Containers an die Anzahl der Levels an
        if anzahl == 0:
            self.ids.bonus_container.height = 0
            return
        reihen = (anzahl + 1) // 2
        hoehe = reihen * 60 + (reihen - 1) * 35 + 20
        self.ids.bonus_container.height = hoehe

    def bonus_button_erstellen(self, level_id, level_name, score, zeit):
        # Baut einen Bonus-Level-Button mit lila Hintergrund
        container = LevelContainerBonus()
        container.size_hint = (None, None)
        container.size = (500, 60)
        container.level_id = level_id
        inhalt = BoxLayout()
        inhalt.orientation = "horizontal"
        inhalt.size_hint = (1, 1)
        inhalt.pos_hint = {"x": 0, "y": 0}
        inhalt.padding = 8
        inhalt.spacing = 0
        blau = (0.09, 0.46, 0.82, 1)
        inhalt.add_widget(self.erstelle_name_label(level_id, level_name, blau))
        inhalt.add_widget(self.bonus_zeit_box(zeit))
        inhalt.add_widget(self.bonus_punkte_box(score))
        container.add_widget(inhalt)
        container.add_widget(self.erstelle_klick_bereich())
        return container

    def bonus_zeit_box(self, zeit):
        # Erstellt die Zeit-Box für Bonus-Levels mit lila Hintergrund
        wrapper = FloatLayout()
        wrapper.size_hint = (None, 1)
        wrapper.width = 140
        box = ScoreBoxBonus()
        box.size_hint = (None, None)
        box.size = (140, 40)
        box.pos_hint = {"center_y": 0.5, "right": 1}
        label = Label()
        label.text = zeit_text(zeit)
        label.font_size = 22
        label.color = (0.09, 0.46, 0.82, 1)
        box.add_widget(label)
        wrapper.add_widget(box)
        return wrapper

    def bonus_punkte_box(self, score):
        # Erstellt die Punkte-Box für Bonus-Levels mit lila Hintergrund
        wrapper = FloatLayout()
        wrapper.size_hint = (None, 1)
        wrapper.width = 40
        box = ScoreBoxBonus()
        box.size_hint = (None, None)
        box.size = (40, 40)
        box.pos_hint = {"center_y": 0.5, "right": 1}
        label = Label()
        label.text = "{0}".format(score)
        label.font_size = 30
        label.color = (0.09, 0.46, 0.82, 1)
        box.add_widget(label)
        wrapper.add_widget(box)
        return wrapper

    def erstelle_klick_bereich(self):
        # Erstellt den unsichtbaren Klick-Button über dem gesamten Container
        btn = Button()
        btn.size_hint = (1, 1)
        btn.pos_hint = {"x": 0, "y": 0}
        btn.background_normal = ""
        btn.background_color = (0, 0, 0, 0)
        btn.bind(on_press=self.bei_knopf_druck)
        return btn

    def erstelle_name_label(self, level_id, level_name, farbe):
        # Erstellt das Label mit Level-Nummer und Name
        label = Label()
        label.text = "{0} - {1}".format(level_id, level_name)
        label.font_size = 30
        label.color = farbe
        label.size_hint_x = 1
        return label

    def erstelle_punkte_box(self, score):
        # Erstellt die quadratische Punktzahl-Box, vertikal zentriert
        wrapper = FloatLayout()
        wrapper.size_hint = (None, 1)
        wrapper.width = 40
        box = ScoreBox()
        box.size_hint = (None, None)
        box.size = (40, 40)
        box.pos_hint = {"center_y": 0.5, "right": 1}
        label = Label()
        label.text = "{0}".format(score)
        label.font_size = 30
        label.color = (0.09, 0.46, 0.82, 1)
        box.add_widget(label)
        wrapper.add_widget(box)
        return wrapper

    def erstelle_zeit_box(self, zeit):
        # Erstellt die Box mit der besten Zeit, links neben der Punktzahl
        wrapper = FloatLayout()
        wrapper.size_hint = (None, 1)
        wrapper.width = 140
        box = ScoreBox()
        box.size_hint = (None, None)
        box.size = (140, 40)
        box.pos_hint = {"center_y": 0.5, "right": 1}
        label = Label()
        label.text = zeit_text(zeit)
        label.font_size = 22
        label.color = (0.09, 0.46, 0.82, 1)
        box.add_widget(label)
        wrapper.add_widget(box)
        return wrapper

    def level_button_erstellen(self, level_id, level_name, score, zeit):
        # Baut den kompletten Level-Button zusammen
        container = LevelContainer()
        container.size_hint = (None, None)
        container.size = (500, 60)
        container.level_id = level_id
        inhalt = BoxLayout()
        inhalt.orientation = "horizontal"
        inhalt.size_hint = (1, 1)
        inhalt.pos_hint = {"x": 0, "y": 0}
        inhalt.padding = 8
        inhalt.spacing = 0
        blau = (0.09, 0.46, 0.82, 1)
        inhalt.add_widget(self.erstelle_name_label(level_id, level_name, blau))
        inhalt.add_widget(self.erstelle_zeit_box(zeit))
        inhalt.add_widget(self.erstelle_punkte_box(score))
        container.add_widget(inhalt)
        container.add_widget(self.erstelle_klick_bereich())
        return container

    def bei_knopf_druck(self, instance):
        # Zeigt Klick-Feedback und öffnet das Level
        container = instance.parent
        self.gewaehltes_level = container.level_id
        level_auswaehlen(self.gewaehltes_level, self.punktzahlen)
        abdunkel_animation(instance)
        Clock.schedule_once(self.level_oeffnen, 0.2)

    def level_oeffnen(self, _dt):
        # Wechselt zum Spiel-Bildschirm
        spiel = self.manager.get_screen("spiel")
        spiel.level_laden(self.gewaehltes_level)
        self.manager.current = "spiel"

    def einkaufsladen_oeffnen_geplant(self, knopf):
        # Zeigt Klick-Feedback und öffnet den Einkaufsladen
        abdunkel_animation(knopf)
        Clock.schedule_once(self.einkaufsladen_oeffnen, 0.2)

    def einkaufsladen_oeffnen(self, _dt):
        # Wechselt zum Einkaufsladen-Bildschirm mit Slide nach links
        laden = self.manager.get_screen("einkaufsladen")
        laden.artikel_anzeigen()
        self.manager.transition = SlideTransition(direction="left", duration=0.3)
        self.manager.current = "einkaufsladen"

    def gesamtpunktzahl_aktualisieren(self):
        # Aktualisiert die drei Übersichts-Felder unten (Level, Zeit, Punkte)
        total = gesamte_punktzahl_berechnen(self.punktzahlen)
        self.ids.total_score_label.text = "Gesamtpunktzahl: {0}".format(total)
        gesamtzeit = gesamte_zeit_berechnen(self.zeiten)
        self.ids.total_time_label.text = "Gesamtzeit: " + zeit_text(gesamtzeit)
        fertige = abgeschlossene_level_zaehlen(self.zeiten)
        alle_levels = aktive_levels_holen()
        anzahl = len(alle_levels)
        text = "Levels abgeschlossen: {0}/{1}".format(fertige, anzahl)
        self.ids.levels_done_label.text = text


###### Einkaufsladen-Bildschirm ######


class EinkaufsladenBildschirm(Screen):
    def __init__(self):
        super().__init__()
        Clock.schedule_once(self.ui_aufbauen, 0)

    def ui_aufbauen(self, _dt):
        # Baut die Shop-Oberfläche auf
        self.artikel_anzeigen()

    def artikel_anzeigen(self):
        # Zeigt alle kaufbaren Artikel im Shop an
        self.ids.level_reihe.clear_widgets()
        self.ids.muell_reihe.clear_widgets()
        self.ids.natur_reihe.clear_widgets()
        einkaeufe = einkaeufe_laden()
        punktzahlen = punktzahlen_laden()
        guthaben = guthaben_berechnen(punktzahlen, einkaeufe)
        self.ids.guthaben_label.text = "Guthaben: {0} Punkte".format(guthaben)
        self.level_artikel_erstellen(einkaeufe, guthaben)
        self.item_artikel_erstellen(einkaeufe, guthaben)

    def level_artikel_erstellen(self, einkaeufe, guthaben):
        # Erstellt die Kauf-Buttons für alle kaufbaren Levels
        for level_id in sorted(KAUFBARE_LEVELS.keys()):
            level = KAUFBARE_LEVELS[level_id]
            name = "Level {0} - {1}".format(level_id, level["name"])
            gekauft = level_id in einkaeufe["levels"]
            leistbar = guthaben >= level["preis"]
            artikel = self.shop_artikel_bauen(name, level["preis"], gekauft, leistbar, 0, 120)
            artikel.size_hint_x = 1
            artikel.kauf_name = level_id
            artikel.kauf_kategorie = "levels"
            artikel.kauf_preis = level["preis"]
            self.ids.level_reihe.add_widget(artikel)

    def item_artikel_erstellen(self, einkaeufe, guthaben):
        # Erstellt die Kauf-Buttons für alle kaufbaren Gegenstände
        for item in KAUFBARE_EINZEL_ITEMS:
            gekauft = item["name"] in einkaeufe["items"]
            leistbar = guthaben >= item["preis"]
            artikel = self.shop_artikel_bauen(item["name"], item["preis"], gekauft, leistbar, 240, 90)
            artikel.kauf_name = item["name"]
            artikel.kauf_kategorie = "items"
            artikel.kauf_preis = item["preis"]
            if item["typ"] == "muell":
                self.ids.muell_reihe.add_widget(artikel)
            else:
                self.ids.natur_reihe.add_widget(artikel)

    def shop_artikel_bauen(self, name, preis, gekauft, leistbar, breite, hoehe):
        # Baut einen einzelnen Shop-Artikel mit Name und Preis
        artikel = ShopArtikel()
        artikel.size_hint = (None, None)
        artikel.size = (breite, hoehe)
        farbe = self.artikel_farbe_bestimmen(gekauft, leistbar)
        artikel.hintergrund_farbe = farbe
        name_label = Label()
        name_label.text = name
        name_label.font_size = 24
        name_label.bold = True
        name_label.color = (0.29, 0.08, 0.55, 1)
        name_label.pos_hint = {"center_x": 0.5, "center_y": 0.6}
        artikel.add_widget(name_label)
        preis_label = self.preis_label_erstellen(preis, gekauft)
        artikel.add_widget(preis_label)
        if not gekauft:
            knopf = self.kauf_knopf_erstellen()
            artikel.add_widget(knopf)
        return artikel

    def artikel_farbe_bestimmen(self, gekauft, leistbar):
        # Gibt die Hintergrundfarbe für einen Shop-Artikel zurück
        if gekauft:
            return (0.78, 0.90, 0.78, 1)
        if leistbar:
            return (0.82, 0.77, 0.91, 1)
        return (0.88, 0.88, 0.88, 1)

    def preis_label_erstellen(self, preis, gekauft):
        # Erstellt das Preis-Label oder "Gekauft"-Label
        label = Label()
        if gekauft:
            label.text = "Gekauft!"
            label.color = (0.10, 0.50, 0.10, 1)
        else:
            label.text = "{0} Punkte".format(preis)
            label.color = (0.29, 0.08, 0.55, 1)
        label.font_size = 20
        label.pos_hint = {"center_x": 0.5, "center_y": 0.25}
        return label

    def kauf_knopf_erstellen(self):
        # Erstellt den unsichtbaren Kauf-Button über einem Artikel
        knopf = Button()
        knopf.size_hint = (1, 1)
        knopf.pos_hint = {"x": 0, "y": 0}
        knopf.background_normal = ""
        knopf.background_color = (0, 0, 0, 0)
        knopf.bind(on_press=self.bei_kauf)
        return knopf

    def bei_kauf(self, instance):
        # Zeigt Klick-Feedback und führt den Kauf durch
        artikel = instance.parent
        punktzahlen = punktzahlen_laden()
        einkaeufe = einkaeufe_laden()
        guthaben = guthaben_berechnen(punktzahlen, einkaeufe)
        if guthaben < artikel.kauf_preis:
            self.abgelehnt_animation(artikel)
            return
        self.kauf_name = artikel.kauf_name
        self.kauf_kategorie = artikel.kauf_kategorie
        abdunkel_animation(instance)
        Clock.schedule_once(self.kauf_abschliessen, 0.2)

    def kauf_abschliessen(self, _dt):
        # Schließt den Kauf ab nach der Animation
        einkauf_durchfuehren(self.kauf_name, self.kauf_kategorie)
        self.artikel_anzeigen()

    def abgelehnt_animation(self, artikel):
        # Schüttelt den Artikel kurz wenn nicht genug Guthaben
        basis_x = artikel.x
        schuetteln = Animation(x=basis_x - 10, duration=0.05)
        schuetteln = schuetteln + Animation(x=basis_x + 10, duration=0.05)
        schuetteln = schuetteln + Animation(x=basis_x - 8, duration=0.05)
        schuetteln = schuetteln + Animation(x=basis_x, duration=0.05)
        schuetteln.start(artikel)

    def zurueck_zum_menue_geplant(self, knopf):
        # Zeigt Klick-Feedback und plant den Wechsel zum Menü
        abdunkel_animation(knopf)
        Clock.schedule_once(self.zurueck_zum_menue, 0.2)

    def zurueck_zum_menue(self, _dt):
        # Geht zurück zum Hauptmenü mit Slide nach rechts
        menu = self.manager.get_screen("menu")
        menu.punktzahlen = punktzahlen_laden()
        menu.zeiten = zeiten_laden()
        menu.level_buttons_erstellen()
        menu.gesamtpunktzahl_aktualisieren()
        self.manager.transition = SlideTransition(direction="right", duration=0.3)
        self.manager.current = "menu"
        Clock.schedule_once(self.fade_wiederherstellen, 0.4)

    def fade_wiederherstellen(self, _dt):
        # Stellt die Fade-Transition für andere Bildschirmwechsel wieder her
        self.manager.transition = FadeTransition(duration=0.2)


###### Spiel-Bildschirm ######


class SpielBildschirm(Screen):
    def __init__(self):
        super().__init__()
        self.gegenstand_widgets = []
        self.ergebnis_overlay = None
        self.aktiver_touch_id = None
        self.aktives_widget = None
        self.touch_offset_x = 0
        self.touch_offset_y = 0
        self.timer_event = None



    ###### Touch-Eingabe ######

    def on_touch_down(self, touch):
        # Startet das Ziehen eines Gegenstands
        if self.ergebnis_overlay is not None:
            return super().on_touch_down(touch)
        if self.aktiver_touch_id is not None:
            return super().on_touch_down(touch)
        for widget in self.gegenstand_widgets:
            if widget.collide_point(touch.x, touch.y):
                self.aktiver_touch_id = touch.uid
                self.aktives_widget = widget
                Animation.cancel_all(widget)
                self.touch_offset_x = widget.x - touch.x
                self.touch_offset_y = widget.y - touch.y
                return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        # Bewegt den Gegenstand mit dem Finger
        if touch.uid == self.aktiver_touch_id:
            self.aktives_widget.x = touch.x + self.touch_offset_x
            self.aktives_widget.y = touch.y + self.touch_offset_y
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        # Lässt den Gegenstand los und prüft die Position
        if touch.uid == self.aktiver_touch_id:
            self.gegenstand_abgelegt(self.aktives_widget)
            self.aktiver_touch_id = None
            self.aktives_widget = None
            return True
        return super().on_touch_up(touch)



    ###### Level laden ######

    def level_laden(self, level_id):
        # Lädt ein Level und startet das Spiel
        logic.spiel_starten(level_id)
        alle_levels = aktive_levels_holen()
        level_data = alle_levels[level_id]
        self.ids.level_titel.text = "{0} - {1}".format(level_id, level_data["name"])
        self.ids.hintergrund.source = level_data["bild"]
        self.alle_gegenstaende_entfernen()
        self.gegenstaende_platzieren()
        self.anzeigen_aktualisieren()
        self.timer_starten()

    def alle_gegenstaende_entfernen(self):
        # Entfernt alle Gegenstands-Widgets vom Bildschirm
        for widget in self.gegenstand_widgets:
            Animation.cancel_all(widget)
            if widget.parent is not None:
                widget.parent.remove_widget(widget)
        self.gegenstand_widgets = []

    def gegenstaende_platzieren(self):
        # Platziert alle Gegenstände des Levels auf dem Bildschirm
        gegenstaende = aktive_gegenstaende_holen(logic.zustand["level_id"])
        spielfeld = self.ids.spielfeld
        for daten in gegenstaende:
            widget = self.gegenstand_widget_erstellen(daten)
            spielfeld.add_widget(widget)
            self.gegenstand_widgets.append(widget)
            self.bewegung_starten(widget)

    def gegenstand_widget_erstellen(self, daten):
        # Erstellt ein einzelnes ziehbares Gegenstands-Widget
        widget = GegenstandWidget()
        widget.source = daten["bild"]
        widget.gegenstand_typ = daten["typ"]
        widget.gegenstand_name = daten["name"]
        widget.bewegung = daten["bewegung"]
        widget.drehung = daten["drehung"]
        seite = BASIS_GROESSE * daten["groesse"]
        widget.size = (seite, seite)
        widget.x = daten["pos_x"] * DESIGN_BREITE
        widget.y = daten["pos_y"] * DESIGN_HOEHE
        widget.start_x = widget.x
        widget.start_y = widget.y
        return widget



    ###### Timer-Anzeige ######

    def timer_starten(self):
        # Startet die Stoppuhr für das aktuelle Level
        self.timer_stoppen()
        logic.timer_starten()
        self.ids.zeit_anzeige.text = zeit_text(0)
        self.timer_event = Clock.schedule_interval(self.timer_aktualisieren, 0.03)

    def timer_aktualisieren(self, _dt):
        # Aktualisiert die angezeigte Zeit
        logic.timer_aktualisieren()
        zeit_ms = int(logic.zustand["laufende_zeit"] * 1000)
        self.ids.zeit_anzeige.text = zeit_text(zeit_ms)

    def timer_stoppen(self):
        # Hält die Stoppuhr an
        if self.timer_event is not None:
            self.timer_event.cancel()
            self.timer_event = None



    ###### Animationen ######

    def bewegung_starten(self, widget):
        # Startet die Bewegung passend zur Flagge des Gegenstands
        if widget.bewegung == "huepfen":
            self.huepfen_starten(widget)
        elif widget.bewegung == "schwingen":
            self.schwingen_starten(widget)
        elif widget.bewegung == "kreisen":
            self.kreisen_starten(widget)

    def huepfen_starten(self, widget):
        # Lässt den Gegenstand auf und ab hüpfen
        animation = Animation(y=widget.start_y + 50, duration=0.5)
        animation = animation + Animation(y=widget.start_y, duration=0.5)
        animation.repeat = True
        animation.start(widget)

    def schwingen_starten(self, widget):
        # Lässt den Gegenstand nach links und rechts schwingen
        animation = Animation(x=widget.start_x - 30, duration=0.5)
        animation = animation + Animation(x=widget.start_x + 30, duration=0.7)
        animation = animation + Animation(x=widget.start_x, duration=0.3)
        animation.repeat = True
        animation.start(widget)

    def kreisen_starten(self, widget):
        # Lässt den Gegenstand in einem runden Kreis fliegen
        animation = None
        schritt = 1
        while schritt <= 12:
            winkel = 2 * math.pi * schritt / 12
            ziel_x = widget.start_x + 30 * math.cos(winkel)
            ziel_y = widget.start_y + 30 * math.sin(winkel)
            teil = Animation(x=ziel_x, y=ziel_y, duration=0.15)
            if animation is None:
                animation = teil
            else:
                animation = animation + teil
            schritt = schritt + 1
        animation.repeat = True
        animation.start(widget)



    ###### Spielablauf ######

    def gegenstand_abgelegt(self, widget):
        # Prüft wo der Gegenstand abgelegt wurde und wertet aus
        rel_x = widget.center_x / DESIGN_BREITE
        rel_y = widget.center_y / DESIGN_HOEHE
        ergebnis = logic.gegenstand_ablegen(widget.gegenstand_typ, rel_x, rel_y)
        if ergebnis["ecke"] == "keine":
            self.gegenstand_zuruecksetzen(widget)
            return
        if ergebnis["richtig"]:
            widget.parent.remove_widget(widget)
            self.gegenstand_widgets.remove(widget)
        else:
            if logic.zustand["leben"] > 0:
                self.alarm_zeigen()
            self.gegenstand_zuruecksetzen(widget)
        self.anzeigen_aktualisieren()
        self.ende_pruefen()

    def gegenstand_zuruecksetzen(self, widget):
        # Setzt den Gegenstand an seinen Platz zurück und startet die Bewegung neu
        widget.x = widget.start_x
        widget.y = widget.start_y
        self.bewegung_starten(widget)

    def anzeigen_aktualisieren(self):
        # Aktualisiert Leben- und Punktzahl-Anzeige
        leben_box = self.ids.leben_anzeige
        leben_box.clear_widgets()
        leben = logic.zustand["leben"]
        fehlende = 3 - leben
        for _i in range(fehlende):
            platzhalter = Label()
            leben_box.add_widget(platzhalter)
        for _i in range(leben):
            herz = Image()
            herz.source = "assets/items/herz.png"
            herz.fit_mode = "contain"
            leben_box.add_widget(herz)
        self.ids.punktzahl_anzeige.text = "Punkte: {0}".format(logic.zustand["punktzahl"])

    def ende_pruefen(self):
        # Prüft ob das Spiel vorbei ist und zeigt das Ergebnis
        if logic.zustand["beendet"]:
            self.ergebnis_zeigen()



    ###### Alarm-Effekte ######

    def alarm_zeigen(self):
        # Zeigt einen roten Sirenen-Alarm in allen vier Bildschirm-Ecken
        ecken = [
            (0, 0), (DESIGN_BREITE, 0),
            (0, DESIGN_HOEHE), (DESIGN_BREITE, DESIGN_HOEHE),
        ]
        for ecke in ecken:
            licht = SirenenLicht()
            licht.size_hint = (None, None)
            licht.size = (340, 340)
            licht.center_x = ecke[0]
            licht.center_y = ecke[1]
            self.ids.spielfeld.add_widget(licht)
            self.alarm_vibrieren(licht)
        Clock.schedule_once(self.alarm_entfernen, 1.0)

    def alarm_vibrieren(self, licht):
        # Lässt ein Sirenen-Licht ganz schnell zittern
        basis_x = licht.x
        basis_y = licht.y
        zittern = Animation(x=basis_x + 9, y=basis_y - 7, duration=0.03)
        zittern = zittern + Animation(x=basis_x - 8, y=basis_y + 8, duration=0.03)
        zittern = zittern + Animation(x=basis_x + 7, y=basis_y + 6, duration=0.03)
        zittern = zittern + Animation(x=basis_x - 9, y=basis_y - 6, duration=0.03)
        zittern = zittern + Animation(x=basis_x, y=basis_y, duration=0.03)
        zittern.repeat = True
        zittern.start(licht)

    def alarm_entfernen(self, _dt):
        # Entfernt alle Sirenen-Lichter wieder vom Spielfeld
        kinder = self.ids.spielfeld.children[:]
        for kind in kinder:
            if isinstance(kind, SirenenLicht):
                Animation.cancel_all(kind)
                self.ids.spielfeld.remove_widget(kind)



    ###### Ergebnis & Navigation ######

    def ergebnis_zeigen(self):
        # Zeigt das Ergebnis-Overlay am Ende des Levels an
        self.timer_stoppen()
        logic.ergebnis_speichern()
        self.ergebnis_overlay = ErgebnisOverlay()
        self.ergebnis_overlay.size_hint = (1, 1)
        self.ergebnis_overlay.pos_hint = {"x": 0, "y": 0}
        if logic.zustand["gewonnen"]:
            titel_text = "Geschafft!"
        else:
            titel_text = "Verloren!"
        self.ergebnis_overlay.add_widget(
            self.ergebnis_label_erstellen(titel_text, 80, 0.6))
        punkte_text = "Punkte: {0}".format(logic.zustand["punktzahl"])
        self.ergebnis_overlay.add_widget(
            self.ergebnis_label_erstellen(punkte_text, 50, 0.45))
        btn = Button()
        btn.text = "Zurück zum Menü"
        btn.font_size = 36
        btn.size_hint = (None, None)
        btn.size = (400, 80)
        btn.pos_hint = {"center_x": 0.5, "center_y": 0.3}
        btn.bind(on_press=self.ergebnis_schliessen)
        self.ergebnis_overlay.add_widget(btn)
        self.ids.spielfeld.add_widget(self.ergebnis_overlay)

    def ergebnis_label_erstellen(self, text, schriftgroesse, mitte_y):
        # Erstellt ein Label für das Ergebnis-Overlay
        label = Label()
        label.text = text
        label.font_size = schriftgroesse
        label.bold = True
        label.size_hint = (None, None)
        label.size = (600, 100)
        label.pos_hint = {"center_x": 0.5, "center_y": mitte_y}
        return label

    def ergebnis_schliessen(self, _instance):
        # Schliesst das Ergebnis und geht zum Menü
        self.zurueck_zum_menue()

    def menue_knopf_gedrueckt(self, knopf):
        # Zeigt Klick-Feedback und plant den Wechsel zum Menü
        abdunkel_animation(knopf)
        Clock.schedule_once(self.menue_wechsel, 0.2)

    def menue_wechsel(self, _dt):
        # Wird nach der Animation aufgerufen
        self.zurueck_zum_menue()

    def zurueck_zum_menue(self):
        # Räumt auf und geht zurück zum Hauptmenü
        self.timer_stoppen()
        if logic.zustand:
            logic.ergebnis_speichern()
        self.alle_gegenstaende_entfernen()
        if self.ergebnis_overlay is not None:
            self.ids.spielfeld.remove_widget(self.ergebnis_overlay)
            self.ergebnis_overlay = None
        menu = self.manager.get_screen("menu")
        menu.punktzahlen = punktzahlen_laden()
        menu.zeiten = zeiten_laden()
        menu.level_buttons_erstellen()
        menu.gesamtpunktzahl_aktualisieren()
        self.manager.current = "menu"


###### App ######


class MuellSammelSimulatorApp(App):
    def build(self):
        # Startet die App und lädt beide Bildschirme
        Builder.load_file("menu.kv")
        Builder.load_file("spiel.kv")
        Builder.load_file("einkaufsladen.kv")
        Window.orientation = "landscape"
        sm = ScreenManager()
        sm.transition = FadeTransition()
        sm.transition.duration = 0.2
        sm.size = (DESIGN_BREITE, DESIGN_HOEHE)
        sm.size_hint = (None, None)
        menu = MenuBildschirm()
        menu.name = "menu"
        spiel = SpielBildschirm()
        spiel.name = "spiel"
        laden = EinkaufsladenBildschirm()
        laden.name = "einkaufsladen"
        sm.add_widget(menu)
        sm.add_widget(spiel)
        sm.add_widget(laden)
        if platform == "android":
            return sm
        return self.skalierung_erstellen(sm)

    def skalierung_erstellen(self, sm):
        # Skaliert die 2000x1200 Design-Auflösung auf den Mac-Bildschirm
        faktor = min(Window.width / DESIGN_BREITE, Window.height / DESIGN_HOEHE)
        skalierung = Scatter()
        skalierung.do_rotation = False
        skalierung.do_translation = False
        skalierung.do_scale = False
        skalierung.scale = faktor
        skalierung.size = (DESIGN_BREITE, DESIGN_HOEHE)
        skalierung.size_hint = (None, None)
        sichtbare_breite = DESIGN_BREITE * faktor
        sichtbare_hoehe = DESIGN_HOEHE * faktor
        x_versatz = (Window.width - sichtbare_breite) / 2
        y_versatz = (Window.height - sichtbare_hoehe) / 2
        skalierung.pos = (x_versatz, y_versatz)
        skalierung.add_widget(sm)
        wurzel = FloatLayout()
        wurzel.add_widget(skalierung)
        return wurzel



if __name__ == "__main__":
    MuellSammelSimulatorApp().run()
