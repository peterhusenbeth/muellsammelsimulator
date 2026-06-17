from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
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
from data import LEVELS, GEGENSTAENDE, punktzahlen_laden, beste_punktzahl_aktualisieren
from logic import gesamte_punktzahl_berechnen, level_auswaehlen
from logic import spiel_starten, ecke_erkennen, gegenstand_pruefen, spiel_beendet



# Styling wird in menu.kv und spiel.kv definiert
class LevelContainer(FloatLayout):
    pass


class ScoreBox(BoxLayout):
    pass


class ErgebnisOverlay(FloatLayout):
    pass


class GegenstandWidget(Image):
    def __init__(self):
        super().__init__()
        self.gegenstand_typ = ""
        self.gegenstand_name = ""
        self.start_x = 0
        self.start_y = 0


class MenuBildschirm(Screen):
    def __init__(self):
        super().__init__()
        self.punktzahlen = punktzahlen_laden()
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
            button = self.level_button_erstellen(level_id, level_data["name"], score)
            if zaehler < 5:
                left_col.add_widget(button)
            else:
                right_col.add_widget(button)
            zaehler = zaehler + 1

    def erstelle_klick_bereich(self):
        # Erstellt den unsichtbaren Klick-Button über dem gesamten Container
        btn = Button()
        btn.size_hint = (1, 1)
        btn.pos_hint = {"x": 0, "y": 0}
        btn.background_normal = ""
        btn.background_color = (0, 0, 0, 0)
        btn.bind(on_press=self.bei_knopf_druck)
        return btn

    def erstelle_name_label(self, level_id, level_name):
        # Erstellt das Label mit Level-Nummer und Name
        label = Label()
        label.text = "{0} - {1}".format(level_id, level_name)
        label.font_size = 20
        label.color = (0.09, 0.46, 0.82, 1)
        label.size_hint_x = 1
        return label

    def erstelle_punkte_box(self, score):
        # Erstellt die quadratische Punktzahl-Box, vertikal zentriert
        wrapper = FloatLayout()
        wrapper.size_hint = (None, 1)
        wrapper.width = 70
        box = ScoreBox()
        box.size_hint = (None, None)
        box.size = (30, 30)
        box.pos_hint = {"center_y": 0.5, "right": 1}
        label = Label()
        label.text = "{0}".format(score)
        label.font_size = 20
        label.color = (0.09, 0.46, 0.82, 1)
        box.add_widget(label)
        wrapper.add_widget(box)
        return wrapper

    def level_button_erstellen(self, level_id, level_name, score):
        # Baut den kompletten Level-Button zusammen
        container = LevelContainer()
        container.size_hint = (None, None)
        container.size = (300, 50)
        container.level_id = level_id
        inhalt = BoxLayout()
        inhalt.orientation = "horizontal"
        inhalt.size_hint = (1, 1)
        inhalt.pos_hint = {"x": 0, "y": 0}
        inhalt.padding = 8
        inhalt.spacing = 5
        inhalt.add_widget(self.erstelle_name_label(level_id, level_name))
        inhalt.add_widget(self.erstelle_punkte_box(score))
        container.add_widget(inhalt)
        container.add_widget(self.erstelle_klick_bereich())
        return container

    def bei_knopf_druck(self, instance):
        # Zeigt Klick-Feedback und öffnet das Level
        container = instance.parent
        self.gewaehltes_level = container.level_id
        level_auswaehlen(self.gewaehltes_level, self.punktzahlen)
        blink = Animation(opacity=0.5, duration=0.08)
        blink = blink + Animation(opacity=1.0, duration=0.08)
        blink.start(container)
        Clock.schedule_once(self.level_oeffnen, 0.2)

    def level_oeffnen(self, _dt):
        # Wechselt zum Spiel-Bildschirm
        spiel = self.manager.get_screen("spiel")
        spiel.level_laden(self.gewaehltes_level)
        self.manager.current = "spiel"

    def gesamtpunktzahl_aktualisieren(self):
        # Aktualisiert die Gesamtpunktzahl-Anzeige
        total = gesamte_punktzahl_berechnen(self.punktzahlen)
        self.ids.total_score_label.text = "Gesamtpunktzahl: {0}".format(total)


class SpielBildschirm(Screen):
    def __init__(self):
        super().__init__()
        self.level_id = None
        self.leben = 3
        self.punktzahl = 0
        self.gegenstand_widgets = []
        self.ergebnis_overlay = None

    def on_touch_down(self, touch):
        # Startet das Ziehen eines Gegenstands
        if self.ergebnis_overlay is not None:
            return super().on_touch_down(touch)
        for widget in self.gegenstand_widgets:
            if widget.collide_point(touch.x, touch.y):
                touch.grab(self)
                touch.ud["widget"] = widget
                touch.ud["offset_x"] = widget.x - touch.x
                touch.ud["offset_y"] = widget.y - touch.y
                return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        # Bewegt den Gegenstand mit dem Finger
        if touch.grab_current == self and "widget" in touch.ud:
            widget = touch.ud["widget"]
            widget.x = touch.x + touch.ud["offset_x"]
            widget.y = touch.y + touch.ud["offset_y"]
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        # Lässt den Gegenstand los und prüft die Position
        if touch.grab_current == self and "widget" in touch.ud:
            touch.ungrab(self)
            widget = touch.ud["widget"]
            self.gegenstand_abgelegt(widget)
            return True
        return super().on_touch_up(touch)

    def level_laden(self, level_id):
        # Lädt ein Level und startet das Spiel
        self.level_id = level_id
        level_data = LEVELS[level_id]
        self.ids.level_titel.text = "{0} - {1}".format(level_id, level_data["name"])
        self.ids.hintergrund.source = level_data["bild"]
        zustand = spiel_starten(level_id)
        self.leben = zustand["leben"]
        self.punktzahl = zustand["punktzahl"]
        self.alle_gegenstaende_entfernen()
        self.gegenstaende_platzieren()
        self.anzeigen_aktualisieren()

    def alle_gegenstaende_entfernen(self):
        # Entfernt alle Gegenstands-Widgets vom Bildschirm
        for widget in self.gegenstand_widgets:
            if widget.parent is not None:
                widget.parent.remove_widget(widget)
        self.gegenstand_widgets = []

    def gegenstaende_platzieren(self):
        # Platziert alle Gegenstände des Levels auf dem Bildschirm
        gegenstaende = GEGENSTAENDE[self.level_id]
        spielfeld = self.ids.spielfeld
        for daten in gegenstaende:
            widget = self.gegenstand_widget_erstellen(daten)
            spielfeld.add_widget(widget)
            self.gegenstand_widgets.append(widget)

    def gegenstand_widget_erstellen(self, daten):
        # Erstellt ein einzelnes ziehbares Gegenstands-Widget
        widget = GegenstandWidget()
        widget.source = daten["bild"]
        widget.gegenstand_typ = daten["typ"]
        widget.gegenstand_name = daten["name"]
        widget.x = daten["pos_x"] * Window.width
        widget.y = daten["pos_y"] * Window.height
        widget.start_x = widget.x
        widget.start_y = widget.y
        return widget

    def gegenstand_abgelegt(self, widget):
        # Prüft wo der Gegenstand abgelegt wurde und wertet aus
        rel_x = widget.center_x / Window.width
        rel_y = widget.center_y / Window.height
        ecke = ecke_erkennen(rel_x, rel_y)
        if ecke == "keine":
            widget.x = widget.start_x
            widget.y = widget.start_y
            return
        ergebnis = gegenstand_pruefen(widget.gegenstand_typ, ecke)
        self.punktzahl = self.punktzahl + ergebnis["punkte"]
        self.leben = self.leben + ergebnis["leben"]
        if ergebnis["richtig"]:
            widget.parent.remove_widget(widget)
            self.gegenstand_widgets.remove(widget)
        else:
            widget.x = widget.start_x
            widget.y = widget.start_y
        self.anzeigen_aktualisieren()
        self.ende_pruefen()

    def anzeigen_aktualisieren(self):
        # Aktualisiert Leben- und Punktzahl-Anzeige
        leben_box = self.ids.leben_anzeige
        leben_box.clear_widgets()
        fehlende = 3 - self.leben
        for _i in range(fehlende):
            platzhalter = Label()
            leben_box.add_widget(platzhalter)
        for _i in range(self.leben):
            herz = Image()
            herz.source = "assets/items/herz.png"
            herz.fit_mode = "contain"
            leben_box.add_widget(herz)
        self.ids.punktzahl_anzeige.text = "Punkte: {0}".format(self.punktzahl)

    def ende_pruefen(self):
        # Prüft ob das Spiel vorbei ist und zeigt das Ergebnis
        if spiel_beendet(self.leben, len(self.gegenstand_widgets)):
            self.ergebnis_zeigen()

    def ergebnis_zeigen(self):
        # Zeigt das Ergebnis-Overlay am Ende des Levels an
        beste_punktzahl_aktualisieren(self.level_id, self.punktzahl)
        self.ergebnis_overlay = ErgebnisOverlay()
        self.ergebnis_overlay.size_hint = (1, 1)
        self.ergebnis_overlay.pos_hint = {"x": 0, "y": 0}
        if self.leben > 0:
            titel_text = "Geschafft!"
        else:
            titel_text = "Verloren!"
        self.ergebnis_overlay.add_widget(
            self.ergebnis_label_erstellen(titel_text, 80, 0.6))
        punkte_text = "Punkte: {0}".format(self.punktzahl)
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

    def zurueck_zum_menue(self):
        # Speichert Punktzahl, räumt auf und geht zurück zum Hauptmenü
        if self.level_id is not None:
            beste_punktzahl_aktualisieren(self.level_id, self.punktzahl)
        self.alle_gegenstaende_entfernen()
        if self.ergebnis_overlay is not None:
            self.ids.spielfeld.remove_widget(self.ergebnis_overlay)
            self.ergebnis_overlay = None
        menu = self.manager.get_screen("menu")
        menu.punktzahlen = punktzahlen_laden()
        menu.level_buttons_erstellen()
        menu.gesamtpunktzahl_aktualisieren()
        self.manager.current = "menu"


class MuelleSammelSimulatorApp(App):
    def build(self):
        # Startet die App und lädt beide Bildschirme
        Builder.load_file("menu.kv")
        Builder.load_file("spiel.kv")
        Window.size = (2000, 1200)
        Window.orientation = "landscape"
        sm = ScreenManager()
        sm.transition = FadeTransition()
        sm.transition.duration = 0.2
        menu = MenuBildschirm()
        menu.name = "menu"
        spiel = SpielBildschirm()
        spiel.name = "spiel"
        sm.add_widget(menu)
        sm.add_widget(spiel)
        return sm

    def on_start(self):
        # Vollbild und Navigationsleiste auf Android verstecken
        if platform == "android":
            Window.fullscreen = True
            Window.borderless = True
            Clock.schedule_once(self.android_vollbild, 0.5)

    def android_vollbild(self, _dt):
        # Versteckt die Android-Navigationsleiste
        from jnius import autoclass
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        View = autoclass("android.view.View")
        aktivitaet = PythonActivity.mActivity
        flags = View.SYSTEM_UI_FLAG_FULLSCREEN
        flags = flags | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
        flags = flags | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
        aktivitaet.getWindow().getDecorView().setSystemUiVisibility(flags)


if __name__ == "__main__":
    MuelleSammelSimulatorApp().run()
