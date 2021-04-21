# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 21:40:39 2021

@author: yanq6
"""

import crossword

import generate

structure = "data/structure1.txt"
words = "data/words1.txt"

crossword = crossword.Crossword(structure, words)
creator = CrosswordCreator(crossword)
creator.enforce_node_consistency()
#creator.revise(x,y)

creator.enforce_node_consistency()
creator.ac3()

creator.solve()

creator.assignment_complete(assignment)





values = []
for v in assignment:
    if assignment[v] is not None:
        for w in assignment[v]:
            if w in values: #not distinct
                print(False)
            if len(w) is not v.length: #length wrong
                print(False)
            if crossword.neighbors(v):
                for neighbor in crossword.neighbors(v):
                    overlaps = crossword.overlaps[v,neighbor]
                    if assignment[neighbor] is not None:
                        for wn in assignment[neighbor]:
                            if w[overlaps[0]] is not wn[overlaps[1]]:
                                print(False)
            values.append(w)
            
            
            
            
if assignment:
    for key in crossword.variables:
        if key in assignment:
            if len(assignment[key]) is not 1:
               print("wrong length")
        else:
            return False
    return True
else:
    return False