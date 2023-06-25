#! /usr/bin/env python

"""
Hauptprogramm für ein "4 gewinnt"-Spiel
"""
__author__ = "Henriette Schulz"
__version__ = "1.0.0"
__email__ = "schulz.henriette.0106@gmail.com"
__status__ = "Prototype"

import spielfeld as sf
import konstanten as ko
import spiel
import ki

import pygame
from pygame.locals import *
import sys

pygame.init()

if __name__ == '__main__':
    titel = str(ko.GEWINNFELDER) + " gewinnt"
    spielfeld = sf.erzeuge_leeres_spielfeld(ko.ZEILEN, ko.SPALTEN)

    # Definieren und Öffnen eines neuen Fensters
    fenster = pygame.display.set_mode((ko.W, ko.H))
    pygame.display.set_caption(titel)
    clock = pygame.time.Clock()

    # setze Spielvariablen und initiale Nachricht
    spieler = spiel.spieler2
    nachricht = spiel.liefere_name(spieler) + " beginnt"
    nachricht2 = "Klicke für nächsten Zug."

    game_over = False
    erster_zug = True
    gewinn_erreicht = False
    zuege_vorbei = False
    zug_erlaubt = True

    # Schleife Hauptprogramm
    while True:
        # Überprüfen, ob Nutzer eine Aktion durchgeführt hat
        for event in pygame.event.get():
            # Beenden bei [ESC] oder [X]
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP and not game_over:
                # Spiellogik
                spielername = spiel.liefere_name(spieler)
                if spielername == "Computer" and ko.KI_MODUS:
                    # Spielfeld löschen
                    fenster.fill(ko.WEISS)
                    # Spielfeld/figuren zeichnen
                    sf.plotte_spielfeld(spielfeld, fenster, nachricht, "Zug wird berechnet.")
                    # Fenster aktualisieren
                    pygame.display.flip()
                    clock.tick(ko.FPS)

                    zug = ki.schlage_naechsten_zug_vor(spielfeld, spieler, erster_zug)
                    erster_zug = False
                    gewinn_erreicht, zug_erlaubt = spiel.mache_zug(spielfeld, spieler, zug["spalte"])
                    zuege_vorbei = not spiel.ist_zug_moeglich(spielfeld)
                    game_over = gewinn_erreicht or zuege_vorbei
                else:
                    pos = pygame.mouse.get_pos()
                    spalte = sf.ermittle_maus_spalte(pos)
                    gewinn_erreicht, zug_erlaubt = spiel.mache_zug(spielfeld, spieler, spalte)
                    zuege_vorbei = not spiel.ist_zug_moeglich(spielfeld)
                    game_over = gewinn_erreicht or zuege_vorbei

                if not zug_erlaubt:
                    nachricht = spiel.liefere_name(spieler) + ": Zug nicht erlaubt"
                elif not game_over:
                    nachricht = "nächster Zug für " + spiel.liefere_name(spiel.liefere_anderen_spieler(spieler))
                else:
                    nachricht2 = "ESC für Spielende"
                    if zuege_vorbei and gewinn_erreicht:
                        nachricht = spiel.liefere_name(spieler) + " gewinnt"
                    elif zuege_vorbei:
                        nachricht = "keine Züge mehr möglich"
                    else:
                        nachricht = spiel.liefere_name(spieler) + " gewinnt"

                # Spieler wechseln
                if zug_erlaubt:
                    spieler = spiel.liefere_anderen_spieler(spieler)

        # Spielfeld löschen
        fenster.fill(ko.WEISS)

        # Spielfeld/figuren zeichnen
        sf.plotte_spielfeld(spielfeld, fenster, nachricht, nachricht2)

        # Fenster aktualisieren
        pygame.display.flip()
        clock.tick(ko.FPS)
