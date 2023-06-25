#! /usr/bin/env python

"""
Implementierung der grundsätzlichen Spielfunktionen für ein "4 gewinnt"-Spiel
"""
__author__ = "Henriette Schulz"
__version__ = "1.0.0"
__email__ = "schulz.henriette.0106@gmail.com"
__status__ = "Prototype"

import spielfeld as sf
import konstanten as ko

spieler1 = ko.SPIELER1       # muss größer sein als spieler2 + Anzahl der Gewinnfelder
spieler2 = ko.SPIELER2


def erzeuge_moegliche_zuege(spielfeld):
    """
    Ermittelt die Spalten und die zugehörigen ersten freien Zeilen, auf denen Züge möglich sind.
    :param spielfeld: Array mit Spielinformationen
    :return: Liste von Dictionaries {"spieler", "zeile", "spalte"}
    """
    return sf.liefere_freie_spalten(spielfeld)


def liefere_name(spieler):
    """
    Liefert die Bezeichnung des Spielers
    :param spieler: ID des Spielers
    :return: Text mit dem Namen des Spielers
    """
    if spieler == spieler1:
        return ko.SPIELERNAME1
    else:
        return ko.SPIELERNAME2


def liefere_anderen_spieler(spieler):
    """
    Liefert die ID des anderen Spielers.
    :param spieler: ID des aktuellen Spielers
    :return: ID des anderen Spielers
    """
    if spieler == spieler1:
        return spieler2
    else:
        return spieler1


def ist_zug_moeglich(spielfeld):
    """
    Prüft, ob noch ein Zug möglich ist.
    :param spielfeld: Array mit Spielinformationen
    :return: True, wenn Zug möglich; sonst False
    """
    if bool(erzeuge_moegliche_zuege(spielfeld)):
        return True
    else:
        return False


def mache_zug(spielfeld, spieler, spalte):
    """
    Führt einen Zug aus.
    :param spielfeld: Array mit Spielinformationen
    :param spieler: aktueller Spieler
    :param spalte: Index der Spalte, wo der Zug ausgeführt wird
    :return: True, wenn der Zug zum Gewinn führt; sonst False; True, wenn Zug erlaubt ist, sonst False
    """

    zug_gewinn, zug_erlaubt = sf.mache_zug(spielfeld, spieler, spalte)
    return zug_gewinn, zug_erlaubt
