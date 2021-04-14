# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 21:40:39 2021

@author: yanq6
"""

import crossword

import generate

structure = "data/structure1.txt"
words = "data/words1.txt"

crossword = Crossword(structure, words)
creator = CrosswordCreator(crossword)
creator.enforce_node_consistency()
#creator.revise(x,y)

creator.enforce_node_consistency()
creator.ac3()







values = []
for v in assignment:
    if assignment[v]:
        for w in assignment[v]:
            if w in values: #not distinct
                print(False)
            if len(w) is not v.length: #length wrong
                print(False)
            for neighbor in crossword.neighbors(v):
                overlaps = crossword.overlaps[v,neighbor]
                for wn in assignment[neighbor]:
                    if w[overlaps[0]] is not wn[overlaps[1]]:
                        print(False)
            values = values.append(w)