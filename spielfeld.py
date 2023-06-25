#! /usr/bin/env python

"""
Funktionen für das Spielfeld für ein "4 gewinnt"-Spiel
"""
__author__ = "Henriette Schulz"
__version__ = "1.0.0"
__email__ = "schulz.henriette.0106@gmail.com"
__status__ = "Prototype"

import numpy
import konstanten as ko

import pygame
from pygame.locals import *


def erzeuge_leeres_spielfeld(zeilen, spalten):
    """
    Erzeugt ein leeres (mit 0 gefülltes) Array als Spielfeld.
    :param zeilen: Anzahl der Zeilen
    :param spalten: Anzahl der Spalten
    :return: zweidimensionales Array als Spielfeld
    """
    return numpy.zeros((zeilen, spalten))


def plotte_spielfeld(spielfeld, fenster, nachricht1, nachricht2):
    """
    Zeichnet das Spielfeld und die Spielfiguren. Gibt eine Nachricht aus.
    :param spielfeld: Array mit den Spielinformationen
    :param fenster: Fenster zum Zeichnen
    :param nachricht1: Text für Statusnachricht groß
    :param nachricht2: Text für Statusnachricht klein
    :return: nichts
    """
    farbe = ko.GRAU
    schrift = pygame.font.SysFont('Arial', 30, True, False)
    schrift_klein = pygame.font.SysFont('Arial', 20, True, False)
    text1 = schrift.render(nachricht1, True, ko.SCHWARZ)
    text2 = schrift_klein.render(nachricht2, True, ko.SCHWARZ)
    fenster.blit(text1, [ko.ABSTAND, ko.H - 80])
    fenster.blit(text2, [ko.ABSTAND, ko.H - 40])

    for z in range(ko.ZEILEN):
        zeile = ko.ZEILEN - z - 1
        for spalte in range(ko.SPALTEN):
            if spielfeld[z, spalte] == 0:
                farbe = ko.GRAU
            if spielfeld[z, spalte] == ko.SPIELER1:
                farbe = ko.ROT
            if spielfeld[z, spalte] == ko.SPIELER2:
                farbe = ko.BLAU

            x = ko.RADIUS + (spalte + 1) * ko.ABSTAND + spalte * 2 * ko.RADIUS
            y = ko.RADIUS + (zeile + 1) * ko.ABSTAND + zeile * 2 * ko.RADIUS

            pygame.draw.circle(fenster, farbe, (x, y), ko.RADIUS)


def liefere_erste_freie_zeile(spielfeld, spalte):
    """
    Liefert die erste unbesetzte Zeile für eine gegebene Spalte.
    :param spielfeld: Array mit den Spielinformationen
    :param spalte: zu untersuchende Spalte
    :return: Index der ersten freien Zeile; -1, wenn keine freie Zeile gefunden
    """
    if spalte >= ko.SPALTEN:
        return -1

    for i in range(ko.ZEILEN):
        if spielfeld[i, spalte] == 0:
            return i

    return -1


def mache_zug(spielfeld, spieler, spalte):
    """
    Führt einen Zug aus.
    :param spielfeld: Array mit Spielinformationen
    :param spieler: aktueller Spieler
    :param spalte: Index der Spalte, wo der Zug ausgeführt wird
    :return: True, wenn der Zug zum Gewinn führt; sonst False; True, wenn Zug möglich, sonst False
    """
    zeile = liefere_erste_freie_zeile(spielfeld, spalte)
    zug_erlaubt = True
    if zeile >= 0:
        spielfeld[zeile, spalte] = spieler
    else: zug_erlaubt = False

    return ist_zug_gewinn(spielfeld, spieler, spalte, zeile), zug_erlaubt


def liefere_freie_spalten(spielfeld):
    """
    Ermittelt die Spalten und die zugehörigen ersten freien Zeilen, auf denen Züge möglich sind.
    :param spielfeld: Array mit Spielinformationen
    :return: Liste von Dictionaries {"spieler", "zeile", "spalte"}
    """
    freie_spalten = []
    for spalte in range(ko.SPALTEN):
        m = {"spieler": 0,
             "zeile": liefere_erste_freie_zeile(spielfeld, spalte),
             "spalte": spalte}

        if m["zeile"] > -1:
            freie_spalten.append(m)  # there are free fields in this column
    return freie_spalten


def ermittle_maus_spalte(pos):
    """
    Ermittelt die Spalte aus der gegebenen x, y-Position
    :param pos: Position (x, y)
    :return: Index der Spalte, auf die geklickt wurde
    """
    x, y = pos
    return int(((x - ko.RADIUS - ko.ABSTAND) / (ko.ABSTAND + 2 * ko.RADIUS)) + 0.5)


def koordinaten_im_feld(spalte, zeile):
    """
    Prüft, ob die Indizes auf dem Spielfeld sind.
    :param spalte: Spaltenindex
    :param zeile: Zeilenindex
    :return: True, wenn auf dem Spielfeld; sonst False
    """
    if (spalte >= 0) and (spalte < ko.SPALTEN) and (zeile >= 0) and (zeile < ko.ZEILEN):
        return True
    else:
        return False


def pruefe_spalte_fuer_gewinn(spielfeld, spieler, spalte, zeile):
    """
    Prüft in gegebener Spalte, ob Gewinnposition für Spieler vorliegt
    :param spielfeld: Array mit Spielinformationen
    :param spieler: Spieler
    :param spalte: zu untersuchende Spalte
    :param zeile: Zeile, auf die nächster Zug fällt
    :return: True für Gewinnposition, sonst False
    """
    gesamt = 0
    for z in range(ko.ZEILEN):
        if (spielfeld[z, spalte] == spieler) or (z == zeile):
            # Das Feld ist von diesem Spieler besetzt.
            # Zähle Feld mit.
            gesamt += 1
            if gesamt == ko.GEWINNFELDER:
                # Anzahl der Gewinnfelder ist erreicht
                return True
        else:
            # Das nächste Feld ist von anderem Spieler besetzt.
            # Fange wieder von vorn an zu zählen.
            gesamt = 0
    return False


def pruefe_zeile_fuer_gewinn(spielfeld, spieler, spalte, zeile):
    """
    Prüft in gegebener Zeile, ob Gewinnposition für Spieler vorliegt
    :param spielfeld: Array mit Spielinformationen
    :param spieler: Spieler
    :param spalte: Spalte, auf die nächster Zug fällt
    :param zeile: zu untersuchende Zeile
    :return: True für Gewinnposition, sonst False
    """
    gesamt = 0
    for s in range(ko.SPALTEN):
        if (spielfeld[zeile, s] == spieler) or (s == spalte):
            # Das Feld ist von diesem Spieler besetzt.
            # Zähle das Feld mit.
            gesamt += 1
            if gesamt == ko.GEWINNFELDER:
                # Anzahl der Gewinnfelder ist erreicht
                return True
        else:
            # Das nächste Feld ist von anderem Spieler besetzt.
            # Fange wieder von vorn an zu zählen.
            gesamt = 0
    return False


def pruefe_diagonale_rechts_oben_links_unten_fuer_gewinn(spielfeld, spieler, spalte, zeile):
    """
    Prüft beabsichtigten Zug in Diagonale von rechts oben nach links unten, ob Gewinnposition für Spieler vorliegt
    :param spielfeld: Array mit Spielinformationen
    :param spieler: Spieler
    :param spalte: Spalte, auf die nächster Zug fällt
    :param zeile: Zeile, auf die nächster Zug fällt
    :return: True für Gewinnposition, sonst False
    """
    gesamt = 0
    # lege Startkoordinaten fest
    z = zeile
    s = spalte

    # suche nach dem Endpunkt in oberer rechter Ecke
    # iteriere nach oben rechts
    while koordinaten_im_feld(s, z):
        z -= 1
        s += 1

    z += 1
    s -= 1

    # iteriere von dort aus nach unten links
    while koordinaten_im_feld(s, z):
        if (spielfeld[z, s] == spieler) or ((z == zeile) and (s == spalte)):
            # Das Feld ist von diesem Spieler besetzt.
            # Zähle das Feld mit.
            gesamt += 1
            if gesamt == ko.GEWINNFELDER:
                # Anzahl der Gewinnfelder ist erreicht
                return True
        else:
            # Das nächste Feld ist von anderem Spieler besetzt.
            # Fange wieder von vorn an zu zählen.
            gesamt = 0

        z += 1
        s -= 1

    return False


def pruefe_diagonale_rechts_unten_links_oben_fuer_gewinn(spielfeld, spieler, spalte, zeile):
    """
    Prüft beabsichtigten Zug in Diagonale von rechts unten nach links oben, ob Gewinnposition für Spieler vorliegt
    :param spielfeld: Array mit Spielinformationen
    :param spieler: Spieler
    :param spalte: Spalte, auf die nächster Zug fällt
    :param zeile: Zeile, auf die nächster Zug fällt
    :return: True für Gewinnposition, sonst False
    """
    gesamt = 0
    # lege Startkoordinaten fest
    z = zeile
    s = spalte

    # suche nach dem Endpunkt in oberer linker Ecke
    # iteriere nach oben links
    while koordinaten_im_feld(s, z):
        z -= 1
        s -= 1

    z += 1
    s += 1

    # iteriere von dort aus nach unten rechts
    while koordinaten_im_feld(s, z):
        if (spielfeld[z, s] == spieler) or ((z == zeile) and (s == spalte)):
            # Das Feld ist von diesem Spieler besetzt.
            # Zähle das Feld mit.
            gesamt += 1
            if gesamt == ko.GEWINNFELDER:
                # Anzahl der Gewinnfelder ist erreicht
                return True
        else:
            # Das nächste Feld ist von anderem Spieler besetzt.
            # Fange wieder von vorn an zu zählen.
            gesamt = 0

        z += 1
        s += 1

    return False


def ist_zug_gewinn(spielfeld, spieler, spalte, zeile):
    """
    Prüft, ob Zug für Spieler zu Gewinn führt.
    :param spielfeld: Array mit Spielinformationen
    :param spieler: Spieler
    :param spalte: Spalte, auf die nächster Zug fällt
    :param zeile: Zeile, auf die nächster Zug fällt
    :return: True für Gewinnposition, sonst False
    """
    return pruefe_spalte_fuer_gewinn(spielfeld, spieler, spalte, zeile) or \
           pruefe_zeile_fuer_gewinn(spielfeld, spieler, spalte, zeile) or \
           pruefe_diagonale_rechts_oben_links_unten_fuer_gewinn(spielfeld, spieler, spalte, zeile) or \
           pruefe_diagonale_rechts_unten_links_oben_fuer_gewinn(spielfeld, spieler, spalte, zeile)


def nehme_zug_zurueck(spielfeld, zug):
    """
    Setzt Feld für gegebenen Zug zurück auf 0 und nimmt damit den Zug zurück.
    :param spielfeld: Array mit Spielinformationen
    :param zug: Spielzug (Dictionary {"spieler", "spalte", "zeile"})
    :return: nichts
    """
    spielfeld[zug["zeile"], zug["spalte"]] = 0
    return


def liefere_benutzte_felder(spielfeld):
    """
    Liefert eine Liste der benutzten Felder.
    :param spielfeld: Array mit Spielinformationen
    :return: Liste von Dictionaries {"spieler", "zeile", "spalte"}
    """
    felder = []
    for spalte in range(ko.SPALTEN):
        for zeile in range(ko.ZEILEN):
            if spielfeld[zeile, spalte] != 0:
                zug = {"spieler": spielfeld[zeile, spalte],
                       "zeile": zeile,
                       "spalte": spalte}
                felder.append(zug)

    return felder
