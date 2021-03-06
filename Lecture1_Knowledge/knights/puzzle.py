from logic import *
import pdb; pdb.set_trace()

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # Game rules
    Or(AKnight,AKnave),
    Not(And(AKnight,AKnave)),
    
    # Puzzle specific
    Implication(AKnight, And(AKnight,AKnave)),
    Implication(AKnave, Not(And(AKnight,AKnave)))
    
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Game rules
    Or(AKnight,AKnave),
    Not(And(AKnight,AKnave)),
    Or(BKnight,BKnave),
    Not(And(BKnight,BKnave)),
    
    # Puzzle specific
    Implication(AKnight, And(AKnave,BKnave)),
    Implication(AKnave, Not(And(AKnave,BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # Game rules
    Or(AKnight,AKnave),
    Not(And(AKnight,AKnave)),
    Or(BKnight,BKnave),
    Not(And(BKnight,BKnave)),
    
    # Puzzle specific
    Implication(AKnight, Or(And(AKnave,BKnave),And(AKnight,BKnight))),
    Implication(AKnave, Not(Or(And(AKnave,BKnave),And(AKnight,BKnight)))),
    
    Implication(BKnight, Or(And(AKnave,BKnight),And(AKnight,BKnave))),
    Implication(BKnave, Not(Or(And(AKnave,BKnight),And(AKnight,BKnave))))
    
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # Game rules
    Or(AKnight,AKnave),
    Not(And(AKnight,AKnave)),
    Or(BKnight,BKnave),
    Not(And(BKnight,BKnave)),
    Or(CKnight,CKnave),
    Not(And(CKnight,CKnave)),
    
    # Puzzle specific
    ## A 
    
    ## B
    Implication(BKnight,And(Implication(AKnight,AKnave),
                            Implication(AKnave,AKnight),
                            CKnave)),
    Implication(BKnave,And(Implication(AKnight,AKnight),
                           Implication(AKnave,AKnave),
                            CKnight)),
    
    
    ## C
    
    Implication(CKnight,AKnight),
    Implication(CKnave,AKnave)
    
        
)


# Puzzle 4
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knight'."
# B says "C is a knave."
# C says "A is a knight."
knowledge4 = And(
    # Game rules
    Or(AKnight,AKnave),
    Not(And(AKnight,AKnave)),
    Or(BKnight,BKnave),
    Not(And(BKnight,BKnave)),
    Or(CKnight,CKnave),
    Not(And(CKnight,CKnave)),
    
    # Puzzle specific
    ## A 
    
    
    
    ## B
    Implication(BKnight,And(Implication(AKnight,AKnight),
                            Implication(AKnave,AKnave),
                            CKnave)),
    Implication(BKnave,And(Implication(AKnight,AKnave),
                           Implication(AKnave,AKnight),
                            CKnight)),
    
    
    ## C
    
    Implication(CKnight,AKnight),
    Implication(CKnave,AKnave)
    
        
)

model = {AKnight.name:True,
         AKnave.name:False,
         BKnight.name:False,
         BKnave.name:True,
         CKnight.name: True,
         CKnave.name:False}


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3),
        ("Puzzle 4", knowledge4)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
