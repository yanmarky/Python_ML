import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
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

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    '''
    node should contain state: movie_i, 
                        parent = movie_j , 
                        action: co-starring person id that lead from Movie i to movie j 
    # first, put all neighbours for source person into queue, check for goal before putting them in
    # take the next state in queue, check goal, if not, find all neighbours in queue, repeat. 
    '''
    
    
    # TODO
    # Keep track of number of movies explored
    num_explored = 0
    # Initialize frontier to just the starting position
    start = Node(state = source, parent = None, action = None)
    frontier = QueueFrontier()
    frontier.add(start)
    # Initialize an empty explored set for person
    explored = set()
    
    # keeo looping until solution found
    while True:
        # if nothing left in the frontier, then no solution
        if frontier.empty():
            path = None
            
        # choose a node from the frontier
        node = frontier.remove()
        num_explored += 1
        
        # if node is the goal, then we have a solution
        if node.state == target:
            path = get_path(node)
            return path
            
        
        # Mark person as explored
        explored.add(node.state)
        
        # Add neighbors to frontier (check goal first)
        for movie_id, person_id in neighbors_for_person(node.state):
            if person_id == target:
                child = Node(state = person_id,parent = node, action = movie_id)
                path = get_path(child)
                return path
            elif not frontier.contains_state(person_id) and person_id not in explored:
                child = Node(state = person_id,parent = node, action = movie_id)
                frontier.add(child)
                
    #raise NotImplementedError


def get_path(node):
    """
    Get path from source to target
    
    Input: Final Node that has state = target
    
    Output: the entire path as a list of (Movie_id1, Perosn_id2), (Movie_id2, Person_id3)....
    
            Person_id2 should co-star with source in Movie_id1
            Person_id3 should co-star with Person_id2 in Movie_id2, and so on
    """
    
    path = []
    while node.parent is not None:
        path.append((node.action,node.state))
        node = node.parent
    path.reverse()
    return path
                
                
                
def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
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
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
