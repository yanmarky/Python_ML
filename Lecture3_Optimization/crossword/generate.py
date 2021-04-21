import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for v in self.domains:
            wordLength = v.length
            wordList_temp = self.domains[v].copy()
            for w in wordList_temp:
                if len(w) != wordLength:
                    self.domains[v].remove(w)
                
        
        #raise NotImplementedError

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        
        # Check for overlaps. If no overlap, then no need revise anythingin x's domain.
        # Note that there can be at most one overlap between each pair of words.
        # Also note that the overlaps dictionary in crossword contains all permutations of v1 and v2. 
        # So it doesn't matter which vatiable goes first.
        overlap = self.crossword.overlaps[x,y]
        
        reviseFlag = False
        
        if overlap == None:
            return reviseFlag
        
        wordList_x_temp = self.domains[x].copy()
         
        for w in wordList_x_temp:
            match = False
            for wy in self.domains[y]: # for each word in x's domain, check conflict with each word in y's domain.
                if w[overlap[0]] == wy[overlap[1]]: 
                    match = True
                    break
            if match == False:     
                self.domains[x].remove(w) # remove if it has conflict with all words in y's domain
                reviseFlag = True
                
        
        return reviseFlag
    
        
        #raise NotImplementedError

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = list()
            for a in self.crossword.overlaps:
                if self.crossword.overlaps[a] is not None:
                    arcs.append(a)
                    
        while len(arcs)>0:
            arc = arcs.pop(0)
            if self.revise(arc[0],arc[1]):
                if len(self.domains[arc[0]])==0:
                    return False
                for neighbor in self.crossword.neighbors(arc[0]):
                    if neighbor is not arc[1]:
                        arcs.append((neighbor,arc[0]))
       
        return True
                
            
            
        
        
        
        
        
        #raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if assignment:
            for key in self.crossword.variables:
                if key not in assignment:
                        return False
            return True
            
        
        
        #raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        
        Assumption: in assignment would be an 1-1 mapping between varaible and their assigned value. 
        
        """
        
        # check for correct length, no conflict, and all values are distinct
        
        values = list()
        for v in assignment:
            if assignment[v] is not None:
                w = assignment[v]
                if w in values: #not distinct
                    #print("Not distinct")
                    return False
                if len(w) is not v.length: #length wrong
                    #print(w)
                    #print(type(w))
                    #print(len(w))
                    #print("Length wrong")
                    return False
                if self.crossword.neighbors(v):
                    for neighbor in self.crossword.neighbors(v):
                        if neighbor in assignment:
                            overlaps = self.crossword.overlaps[v,neighbor]
                            if assignment[neighbor] is not None:
                                wn = assignment[neighbor]
                                if w[overlaps[0]] is not wn[overlaps[1]]:
                                    #print(f"Conflict with {neighbor},{overlaps}")
                                    return False
                    values.append(w)
        return True
    
        
        
        
        #raise NotImplementedError

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        varList = []
        for w in self.domains[var]:
            count = 0
            if self.crossword.neighbors(var):
                for neighbor in self.crossword.neighbors(var):
                    if neighbor not in assignment:
                        overlap = self.crossword.overlaps[var,neighbor]
                        for wn in self.domains[neighbor]:
                            if w[overlap[0]] is not wn[overlap[1]]:
                                count += 1
            varList.append((w,count))
        return [i for i,j in sorted(varList, key = lambda l:l[1]) ]
                        
                        
        
        
        #raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        varList = []
        for v in self.crossword.variables:
            if v not in assignment:
                varList.append((v,len(self.domains[v]),len(self.crossword.neighbors(v))))
        
        return [i for i,j,k in sorted(varList, key = lambda l:(l[1],-l[2]))].pop(0)         
        
        
        #raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        #print(assignment)
        if self.assignment_complete(assignment):
            return assignment
        
        var = self.select_unassigned_variable(assignment)
        #print(var)
        #assignment_temp = assignment.copy()
        for w in self.order_domain_values(var, assignment):
            assignment[var] = w
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result:
                    return result
            assignment.pop(var)
        return None    
            
              
        #raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
