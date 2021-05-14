import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP
AP -> Adj | Adj AP
PP -> P NP
NP -> N | Det N | Det AP N | AP NP  | NP PP | NP Adv
VP -> V | V NP | V NP PP | VP Conj NP VP | VP Conj VP | Adv VP | VP PP | VP Adv
    
    
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    wordList = [word.lower() for word in nltk.word_tokenize(sentence) if any(c.isalpha() for c in word)]
    return wordList

    #raise NotImplementedError


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    npList = []
    for subtree in tree.subtrees():
        #print(subtree)
        if subtree.label()=="NP": #Check if any subtree also contains a tree with label "NP"
            final_NP = True
            height = subtree.height()
            for t in subtree.subtrees(lambda x: x.height() < height):
               # print(t)
                if t.label()=="NP":
                    #print(t.label())
                    final_NP = False
                    break
            if final_NP:
                #npList.append(" ".join(subtree.leaves()))
                npList.append(subtree)
    return npList
    #raise NotImplementedError


if __name__ == "__main__":
    main()
