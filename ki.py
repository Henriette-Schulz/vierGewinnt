#! /usr/bin/env python

"""
Funktionen für eine künstliche Intelligenz für ein "4 gewinnt"-Spiel
"""
__author__ = "Henriette Schulz"
__version__ = "1.0.0"
__email__ = "schulz.henriette.0106@gmail.com"
__status__ = "Prototype"

import spielfeld as sf
import konstanten as ko
import spiel
import performance
import random
import numpy
import time

spieler1 = spiel.spieler1
spieler2 = spiel.spieler2

gespeicherter_zug = {"spieler": 100,
                     "zeile": 0,
                     "spalte": 0}


def bewerte_zelle(spielfeld, spieler, zelle):
    """
    Bewertet Zug für den MinMax-Algorithmus.
    :param spielfeld: Array mit Spielinformationen
    :param spieler: ID für Spieler
    :param zelle: Zelle als Dictionary {"spieler", "zeile", "spalte"}
    :return: 10, wenn Spieler gewinnt; -10, wenn anderer Spieler gewinnt; sonst 0
    """
    wert = 10
    if spieler != zelle["spieler"]:
        wert = -10

    if sf.ist_zug_gewinn(spielfeld, zelle["spieler"], zelle["spalte"], zelle["zeile"]):
        # Gewinn erkannt
        return wert
    else:
        return 0


def suche_gewinnposition(spielfeld, spieler, p):
    """
    Bewertet das gesamte Spielfeld, ob ein Spieler gewonnen hat.
    :param spielfeld: Array mit Spielinformationen
    :param spieler: ID für zu untersuchenden Spieler
    :param p: Objekt für Performanceinformationen
    :return: 10, wenn Spieler gewinnt; -10, wenn anderer Spieler gewinnt; sonst 0
    """
    felder = sf.liefere_benutzte_felder(spielfeld)
    p.untersuchte_stellungen += 1

    for feld in felder:
        w = bewerte_zelle(spielfeld, spieler, feld)
        if w != 0:
            return w

    return 0


def zaehle_anzahl_in_zeile(spielfeld, spieler, anzahl):
    """
    Zählt die Zahl der Steine in einer Zeile für Spieler - jeweils für 1 bis anzahl.
    :param spielfeld: Array mit Spielinformationen
    :param spieler: ID für Spieler
    :param anzahl: Max. Anzahl der Steine, die gezählt werden sollen
    :return: Array (0...anzahl-1) mit jeweiliger Zahl der gezählten Steine
    """
    gesamt = numpy.zeros(anzahl)
    zaehler = numpy.zeros(anzahl)

    for z in range(ko.ZEILEN):
        for s in range(ko.SPALTEN):
            if spielfeld[z, s] == spieler:
                # Das Feld ist von diesem Spieler besetzt.
                # Zähle das Feld mit.

                for i in range(anzahl):
                    zaehler[i] += 1
                    if zaehler[i] == i + 1:
                        # Anzahl der Gewinnfelder ist erreicht
                        gesamt[i] += 1
            else:
                # Das nächste Feld ist von anderem Spieler besetzt.
                # Fange wieder von vorn an zu zählen.
                zaehler = numpy.zeros(anzahl)
    return gesamt


def berechne_wert(bewertung):
    """
    Berechnet einen gewichteten Wert je Anzahl der Spielsteine in einer Zeile.
    :param bewertung: Liste mit Anzahlen für Einer, Zweier usw.
    :return: gewichteter Wert
    """
    wert = 0
    for i in range(ko.GEWINNFELDER - 1):
        wert += bewertung[i] * ko.GEWICHT[i]
    return wert


def bewerte_spiel(spielfeld, spieler, p):
    """
    Bewertet das gesamte Spielfeld, ob ein Spieler gewonnen hat.
    :param spielfeld: Array mit Spielinformationen
    :param spieler: ID für zu untersuchenden Spieler
    :param p: Objekt für Performanceinformationen
    :return: 50000, wenn Spieler gewinnt; -50000, wenn anderer Spieler gewinnt; sonst Zwischenwert
    """
    wert_vier = suche_gewinnposition(spielfeld, spieler, p)
    if wert_vier != 0:
        return wert_vier * ko.GEWICHT[ko.GEWINNFELDER - 1]

    bewertung_z1 = zaehle_anzahl_in_zeile(spielfeld, spieler, ko.GEWINNFELDER)
    wert_s1 = berechne_wert(bewertung_z1)
    bewertung_z2 = zaehle_anzahl_in_zeile(spielfeld, spiel.liefere_anderen_spieler(spieler), ko.GEWINNFELDER)
    wert_s2 = berechne_wert(bewertung_z2)

    if spiel.liefere_name(spieler) == "Computer":
        wert_s1 = int(wert_s1 * 1.1)
    else:
        wert_s2 = int(wert_s2 * 1.1)

    wert = wert_s2 - wert_s1

    p.untersuchte_stellungen += 1

    return wert


def fuehre_naechsten_zug_aus(spielfeld, spieler, zuege, index):
    """
    Führt den nächsten Zug aus einer Liste von Zügen aus.
    :param spielfeld: Array mit Spielinformationen
    :param spieler: ID für Spieler
    :param zuege: Liste der möglichen Züge
    :param index: Index für den nächsten Zug
    :return: nächster Zug als Dictionary {"spieler", "zeile", "spalte"}
    """
    if bool(zuege):
        naechster_zug = zuege.pop(index)
        spalte = naechster_zug["spalte"]
        sf.mache_zug(spielfeld, spieler, spalte)

        return naechster_zug
    else:
        return None


def maxx(spielfeld, spieler, tiefe, alpha, beta, p):
    """
    Stellt die MAX-Methode für den MinMax-Algorithmus bereit.
    Liefert die Bewertung zurück und speichert den optimalen Zug in einer globalen Variable gespeicherter_zug.
    :param spielfeld: Array mit Spielinformationen
    :param spieler: ID für Spieler
    :param tiefe: Suchtiefe
    :param alpha: Parameter für Alpha-Beta-Suche
    :param beta: Parameter für Alpha-Beta-Suche
    :param p: Objekt für Performanceinformationen
    :return: Bewertung des Spielstandes
    """
    moegliche_zuege = spiel.erzeuge_moegliche_zuege(spielfeld)

    p.max_aufrufe += 1

    if (tiefe == 0) or (not bool(moegliche_zuege)):
        wert = bewerte_spiel(spielfeld, spieler, p)
        return wert

    max_wert = alpha

    while bool(moegliche_zuege):
        index = int(len(moegliche_zuege) / 2)
        zug = moegliche_zuege[index]
        fuehre_naechsten_zug_aus(spielfeld, spieler, moegliche_zuege, index)
        wert = minn(spielfeld, spiel.liefere_anderen_spieler(spieler), tiefe - 1, max_wert, beta, p)
        sf.nehme_zug_zurueck(spielfeld, zug)

        if wert > max_wert:
            max_wert = wert
            if tiefe == ko.TIEFE:
                global gespeicherter_zug
                gespeicherter_zug = zug
            if max_wert >= beta:
                break

    return max_wert


def minn(spielfeld, spieler, tiefe, alpha, beta, p):
    """
    Stellt die MIN-Methode für den MinMax-Algorithmus bereit.
    :param spielfeld: Array mit Spielinformationen
    :param spieler: ID für Spieler
    :param tiefe: Suchtiefe
    :param alpha: Parameter für Alpha-Beta-Suche
    :param beta: Parameter für Alpha-Beta-Suche
    :param p: Objekt für Performanceinformationen
    :return: Bewertung des Spielstandes
    """
    p.min_aufrufe += 1
    moegliche_zuege = spiel.erzeuge_moegliche_zuege(spielfeld)

    if (tiefe == 0) or (not bool(moegliche_zuege)):
        wert = bewerte_spiel(spielfeld, spieler, p)
        return wert

    min_wert = beta

    while bool(moegliche_zuege):
        index = int(len(moegliche_zuege) / 2)
        zug = moegliche_zuege[index]
        fuehre_naechsten_zug_aus(spielfeld, spieler, moegliche_zuege, index)
        wert = maxx(spielfeld, spiel.liefere_anderen_spieler(spieler), tiefe - 1, alpha, min_wert, p)
        sf.nehme_zug_zurueck(spielfeld, zug)

        if wert < min_wert:
            min_wert = wert
            if min_wert <= alpha:
                break

    return min_wert


def gebe_performance_aus(zug_spalte, max_wert, p, laufzeit, spieler, zufall, erster_zug=False):
    """
    Gibt die Performancewerte in einer Zeile, ggf. mit Überschrift, aus.
    :param zug_spalte: Spalte des Zuges
    :param max_wert: Wert der MinMax-Funktion
    :param p: Objekt mit Performancewerten
    :param laufzeit: Laufzeit
    :param spieler: ID für Spieler
    :param zufall: True, wenn zufälliger Zug, sonst False
    :param erster_zug: Wenn True, wird Überschrift ausgegeben.
    :return: nichts
    """
    # bereite Überschrift vor
    if erster_zug:
        ueberschriften = ["Zug in Spalte", "Gewinnzug", "Zufall", "Max. Wert", "Aufrufe Max", "Aufrufe Min",
                          "Stellungen", "Laufzeit [s]"]
        ueberschrift = ""
        for u in ueberschriften:
            ueberschrift += f"{u:<15}" + "\t"

        print(ko.FETT + ueberschrift + ko.FETT_ENDE)

    # bereite Ergebniszeile vor
    laufzeit_string = f"{laufzeit:.2f}"
    zufall_string = "n/a"
    if zufall:
        zufall_string = "ja"

    if (spieler == ko.SPIELER1) or (spieler == ko.SPIELER2):
        ergebnisse = [zug_spalte, spiel.liefere_name(spieler), zufall_string, "n/a", 0, 0, 0, laufzeit_string]
    else:
        ergebnisse = [zug_spalte, "n/a", zufall_string, max_wert, p.max_aufrufe, p.min_aufrufe,
                      p.untersuchte_stellungen, laufzeit_string]

    ergebnis = ""
    for e in ergebnisse:
        ergebnis += f"{e:<15}" + "\t"

    print(ergebnis.replace('.', ','))


def schlage_naechsten_zug_vor(spielfeld, spieler, erster_zug):
    """
    Schlägt den nächsten Zug für einen gegebenen Spieler vor.
    :param spielfeld: Array mit Spielinformationen
    :param spieler: ID für Spieler
    :param erster_zug: True, wenn erster Zug, sonst False
    :return: Zug als Dictionary {"spieler", "zeile", "spalte"}
    """
    t0 = time.time()
    p = performance.PerformanceZahlen()

    moegliche_zuege = spiel.erzeuge_moegliche_zuege(spielfeld)

    # Gewinnt Spieler sofort mit diesem Zug?
    for zug in moegliche_zuege:
        zug["spieler"] = spieler
        if sf.ist_zug_gewinn(spielfeld, zug["spieler"], zug["spalte"], zug["zeile"]):
            t1 = time.time()
            laufzeit = t1 - t0
            gebe_performance_aus(zug["spalte"], 0, p, laufzeit, spieler, False, erster_zug)
            return zug

    # Verhindert der Zug den Gewinn des Gegners?
    for zug in moegliche_zuege:
        gegner = spiel.liefere_anderen_spieler(spieler)
        zug["spieler"] = gegner
        raus = sf.ist_zug_gewinn(spielfeld, zug["spieler"], zug["spalte"], zug["zeile"])
        if raus:
            t1 = time.time()
            laufzeit = t1 - t0
            gebe_performance_aus(zug["spalte"], 0, p, laufzeit, gegner, False, erster_zug)
            return zug

    max_wert = maxx(spielfeld, spieler, ko.TIEFE, -65000, 65000, p)

    t1 = time.time()
    laufzeit = t1 - t0

    if int(max_wert) == 0:
        # keine Gewinnstellung erkannt, mache zufälligen Zug
        zufall = random.randint(0, len(moegliche_zuege) - 1)
        zug = moegliche_zuege[zufall]
        gebe_performance_aus(zug["spalte"], max_wert, p, laufzeit, 0, True, erster_zug)
        return zug

    elif int(max_wert) == -50000:
        # mit dem nächsten Zug gewinnt der Gegner, also vermeiden, wenn möglich
        verlust = gespeicherter_zug["spalte"]
        # Falls nur noch ein Zug möglich ist, dann muss er gemacht werden. Sonst vermeiden.
        if len(moegliche_zuege) <= 1:
            zug = gespeicherter_zug
        else:
            # Suche den Verlustzug aus den möglichen Zügen heraus und eliminiere ihn.
            for i in range(len(moegliche_zuege)):
                mz = moegliche_zuege[i]
                if mz["spalte"] == verlust:
                    moegliche_zuege.pop(i)
                    break
            # Wenn nur noch ein Zug übrig bleibt, mache diesen. Sonst zufälligen möglichen Zug machen.
            if len(moegliche_zuege) <= 1:
                index = 0
            else:
                index = random.randint(0, len(moegliche_zuege) - 1)
            zug = moegliche_zuege[index]
        gebe_performance_aus(zug["spalte"], max_wert, p, laufzeit, 0, True, erster_zug)
        return zug

    else:
        gebe_performance_aus(gespeicherter_zug["spalte"], max_wert, p, laufzeit, 0, False, erster_zug)

    return gespeicherter_zug
