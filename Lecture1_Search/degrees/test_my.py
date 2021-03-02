#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 01:26:14 2021

@author: qingxiangyan
"""
import csv
import sys

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


f = open(f"/Users/qingxiangyan/Documents/github_repo/Python_ML/degrees/large/people.csv",encoding ="utf-8")

reader = csv.DictReader(f)
for row in reader:
    people[row["id"]] = {
            "name": row["name"],
            "birth": row["birth"],
            "movies": set()
            }
    if row["name"].lower() not in names:
        names[row["name"].lower()] = {row["id"]}
    else:
        names[row["name"].lower()].add(row["id"])
                    

f = open(f"/Users/qingxiangyan/Documents/github_repo/Python_ML/degrees/large/movies.csv",encoding ="utf-8")

reader = csv.DictReader(f)

for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
f = open(f"/Users/qingxiangyan/Documents/github_repo/Python_ML/degrees/large/stars.csv",encoding ="utf-8")

reader = csv.DictReader(f)
for row in reader:
    try:
        people[row["person_id"]]["movies"].add(row["movie_id"])
        movies[row["movie_id"]]["stars"].add(row["person_id"])
    except KeyError:
        pass

name = "Emma Watson"

person_ids = list(names.get(name.lower(), set()))
if len(person_ids) == 0:
    source = None
elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                source = person_id
        except ValueError:
            pass
        source = None
else:
        source = person_ids[0]
        
name = "Jennifer Lawrence"    
person_ids = list(names.get(name.lower(), set()))
if len(person_ids) == 0:
    target = None
elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                target = person_id
        except ValueError:
            pass
        target = None
else:
        target = person_ids[0]    
        
person_id = node.state
        
movie_ids = people[person_id]["movies"]
neighbors = set()
for movie_id in movie_ids:
   for person_id in movies[movie_id]["stars"]:
       neighbors.add((movie_id, person_id))       
       
  # choose a node from the frontier
        node = frontier.remove()
        num_explored += 1
        
        # if node is the goal, then we have a solution
        if node.state == target:
            path = get_path(node)
            return path
            
        
        # Mark person as explored
        explored.add(node.state)      
for movie_id, person_id in neighbors:
    if person_id == target:
        child = Node(state = person_id,parent = node, action = movie_id)
        path = get_path(child)
    elif not frontier.contains_state(person_id) and person_id not in explored:
        child = Node(state = person_id,parent = node, action = movie_id)
        frontier.add(child)      
        
movie_ids = people[person_id]["movies"]
neighbors = set()
for movie_id in movie_ids:
   for person_id in movies[movie_id]["stars"]:
       neighbors.add((movie_id, person_id))        
        

###################
# Functions
###################
