#! /usr/bin/env python

"""
Objekt zum Speichern von Performancezahlen für ein "4 gewinnt"-Spiel
"""
__author__ = "Henriette Schulz"
__version__ = "1.0.0"
__email__ = "schulz.henriette.0106@gmail.com"
__status__ = "Prototype"


class PerformanceZahlen(object):
    def __init__(self):
        self.min_aufrufe = 0
        self.max_aufrufe = 0
        self.untersuchte_stellungen = 0
