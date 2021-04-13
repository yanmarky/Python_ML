#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 18:39:44 2021

@author: qingxiangyan
"""


from minesweeper import *


game = Minesweeper(3,3,2)

agent = MinesweeperAI(game.height, game.width)

move = (2,2)

agent.add_knowledge(move,game.nearby_mines(move))

for k in agent.knowledge:
    print(k)
    
    
move = agent.make_safe_move()

if move == None:
    move = agent.make_random_move()
    
move = (2,0)

agent.add_knowledge(move,game.nearby_mines(move))

for k in agent.knowledge:
    print(k)
    
move = (2,1)
agent.add_knowledge(move,game.nearby_mines(move))
for k in agent.knowledge:
    print(k)
    
    
move = (1,1)
agent.add_knowledge(move,game.nearby_mines(move))
for k in agent.knowledge:
    print(k)
    
move = (0,2)
agent.add_knowledge(move,game.nearby_mines(move))
for k in agent.knowledge:
    print(k)