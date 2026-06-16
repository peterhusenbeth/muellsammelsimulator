from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.animation import Animation
from data import LEVELS, punktzahlen_laden, punktzahlen_speichern
from logic import gesamte_punktzahl_berechnen, level_auswaehlen


# Styling wird in menu.kv und spiel.kv definiert
class LevelContainer(FloatLayout):
    pass


class ScoreBox(BoxLayout):
    pass


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
        label.font_size = 36
        label.color = (0, 0, 0, 1)
        label.size_hint_x = 0.65
        return label

    def erstelle_punkte_box(self, score):
        # Erstellt die Punktzahl-Box mit Label auf der rechten Seite
        box = ScoreBox()
        box.size_hint_x = 0.35
        box.padding = 5
        label = Label()
        label.text = "Punkte: {0}".format(score)
        label.font_size = 30
        label.color = (0, 0, 0, 1)
        box.add_widget(label)
        return box

    def level_button_erstellen(self, level_id, level_name, score):
        # Baut den kompletten Level-Button zusammen
        container = LevelContainer()
        container.size_hint = (None, None)
        container.size = (610, 190)
        container.level_id = level_id
        inhalt = BoxLayout()
        inhalt.orientation = "horizontal"
        inhalt.size_hint = (1, 1)
        inhalt.pos_hint = {"x": 0, "y": 0}
        inhalt.padding = 10
        inhalt.spacing = 10
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

    def level_laden(self, level_id):
        # Lädt ein Level und zeigt Hintergrund und Titel an
        self.level_id = level_id
        level_data = LEVELS[level_id]
        self.ids.level_titel.text = "{0} - {1}".format(level_id, level_data["name"])
        self.ids.hintergrund.source = level_data["bild"]

    def zurueck_zum_menue(self):
        # Geht zurück zum Hauptmenü
        self.manager.current = "menu"


class MuelleSammelSimulatorApp(App):
    def build(self):
        # Startet die App und lädt beide Bildschirme
        Builder.load_file("menu.kv")
        Builder.load_file("spiel.kv")
        Window.size = (2000, 1200)
        Window.orientation = "landscape"
        sm = ScreenManager()
        menu = MenuBildschirm()
        menu.name = "menu"
        spiel = SpielBildschirm()
        spiel.name = "spiel"
        sm.add_widget(menu)
        sm.add_widget(spiel)
        return sm


if __name__ == "__main__":
    MuelleSammelSimulatorApp().run()
