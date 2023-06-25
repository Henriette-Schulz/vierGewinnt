#! /usr/bin/env python

"""
Definition von globalen Konstanten für ein "4 gewinnt"-Spiel
"""
__author__ = "Henriette Schulz"
__version__ = "1.0.0"
__email__ = "schulz.henriette.0106@gmail.com"
__status__ = "Prototype"

TIEFE = 6  # Suchtiefe

SPALTEN = 7  # Spaltenzahl
ZEILEN = 6  # Zeilenzahl
GEWINNFELDER = 4  # Anzahl der Gewinnfelder

GEWICHT = [1, 15, 400, 5000]  # Gewichte für Bewertungsfunktion

RADIUS = 30  # Radius für Kreise auf dem Spielfeld
ABSTAND = 10  # Abstand zwischen den Kreisen und zum Rand

W = SPALTEN * (2 * RADIUS + ABSTAND) + ABSTAND  # Breite des Spielfelds in Pixels
H = ZEILEN * (2 * RADIUS + ABSTAND) + ABSTAND + 100  # Höhe des Spielfeldes in Pixels
FPS = 60  # Bildwiederholrate für Fenster

# Farbdefinitionen
WEISS = (255, 255, 255)
SCHWARZ = (0, 0, 0)
GRAU = (220, 220, 220)
ROT = (237, 125, 49)
BLAU = (68, 114, 196)

FETT = '\033[1m'  # fette Ausgabe von Strings
FETT_ENDE = '\033[0m'  # Ende der fetten Ausgabe

SPIELER1 = 1  # ID für Spieler 1
SPIELER2 = 2  # ID für Spieler 2

KI_MODUS = True  # Computer soll Züge machen

if KI_MODUS:
    SPIELERNAME2 = "Spieler"
    SPIELERNAME1 = "Computer"  # Spieler 1 beginnt immer, wenn "Computer", dann beginnt dieser
else:
    SPIELERNAME1 = "Spieler 1"  # Name für Spieler 1
    SPIELERNAME2 = "Spieler 2"  # Name für Spieler 2
