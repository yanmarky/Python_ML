import csv
import itertools
import sys
from pomegranate import *

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}

# Build Bayesnet model:

parent1 = Node(DiscreteDistribution({
    2: PROBS["gene"][2],
    1: PROBS["gene"][1],
    0: PROBS["gene"][0]
}), name="parent1")

parent2 = Node(DiscreteDistribution({
    2: PROBS["gene"][2],
    1: PROBS["gene"][1],
    0: PROBS["gene"][0]
}), name="parent2")


passedGene = Node(ConditionalProbabilityTable([
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 0, 2, 0],
    [0, 1, 0, 0.5],
    [0, 1, 1, 0.5],
    [0, 1, 2, 0],
    [0, 2, 0, 0],
    [0, 2, 1, 1],
    [0, 2, 2, 0],
    [1, 0, 0, 0.5],
    [1, 0, 1, 0.5],
    [1, 0, 2, 0],
    [1, 1, 0, 0.25],
    [1, 1, 1, 0.5],
    [1, 1, 2, 0.25],
    [1, 2, 0, 0],
    [1, 2, 1, 0.5],
    [1, 2, 2, 0.5],
    [2, 0, 0, 0],
    [2, 0, 1, 1],
    [2, 0, 2, 0],
    [2, 1, 0, 0],
    [2, 1, 1, 0.5],
    [2, 1, 2, 0.5],
    [2, 2, 0, 0],
    [2, 2, 1, 0],
    [2, 2, 2, 1],
  
], [parent1.distribution, parent2.distribution]), name="passedGene")

childGene = Node(ConditionalProbabilityTable([
    [0, 0, (1-PROBS["mutation"])*(1-PROBS["mutation"])],
    [0, 1, 2*PROBS["mutation"]*(1-PROBS["mutation"])],
    [0, 2, PROBS["mutation"]*PROBS["mutation"]],
    [1, 0, PROBS["mutation"]*(1-PROBS["mutation"])],
    [1, 1, (1-PROBS["mutation"])*(1-PROBS["mutation"])+PROBS["mutation"]*PROBS["mutation"]],
    [1, 2, PROBS["mutation"]*(1-PROBS["mutation"])],
    [2, 0, PROBS["mutation"]*PROBS["mutation"]],
    [2, 1, 2*PROBS["mutation"]*(1-PROBS["mutation"])],
    [2, 2, (1-PROBS["mutation"])*(1-PROBS["mutation"])],
 ], [passedGene.distribution]), name="childGene")   

model = BayesianNetwork()
model.add_states(parent1, parent2, passedGene, childGene)

# Add edges connecting nodes
model.add_edge(parent1, passedGene)
model.add_edge(parent2, passedGene)
model.add_edge(passedGene, childGene)

# Finalize model
model.bake()

def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information 
        ## Find the subset of people whose trait is None, or True
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue
        #print(have_trait)
        
        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # 1: for Probability of number of genes, if parents, use uncondicional probability; 
    #    if child, write a separate function to calculate the prob dist. conditional on parents status
    # 2: For probability of trait, use the conditional probability table
    # 3: Same for people not in "have_trait" 
    
    # Initialize status dict to store gene/trait status for everyone
    status = get_status(people, one_gene, two_genes, have_trait)
        
    # calculating joint probability
    pgene = 1
    ptrait = 1
    #Calculating probability for number of genes
    for p in status:
        if people[p]['mother'] == None and people[p]['father'] == None:
            pgene_temp = PROBS["gene"][status[p]["gene"]]
            pgene = pgene * pgene_temp
        else:
            predictions = model.predict_proba({
                "parent2": status[people[p]['mother']]["gene"],
                "parent1": status[people[p]['father']]["gene"]
            })
            for node, prediction in zip(model.states, predictions):
                if node.name == "childGene":
                    p_temp = prediction.parameters[0]    
            pgene_temp = p_temp[status[p]["gene"]]
            pgene = pgene * pgene_temp
     
    #Calculating probability for traits:
    for p in status:
        ptrait_temp = PROBS["trait"][status[p]["gene"]][status[p]["trait"]] 
        ptrait = ptrait * ptrait_temp
        
    joint_p = pgene * ptrait
    return joint_p

    
    #raise NotImplementedError


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    status = get_status(probabilities, one_gene, two_genes, have_trait)
    
    for person in probabilities:
        probabilities[person]["gene"][status[person]["gene"]] += p
        probabilities[person]["trait"][status[person]["trait"]] += p
    
    
    
    #raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        for item in probabilities[person]:
            norm_factor = sum(probabilities[person][item].values())
            for prob in probabilities[person][item]:
                probabilities[person][item][prob] = probabilities[person][item][prob]/norm_factor
    
    
    
    #raise NotImplementedError


def get_status(people, one_gene, two_genes, have_trait):
    """
    create a dictionary to store everyone's gene and trait status

    """
    
    
    status = {}
    names = list(people.keys())
    
    for n in names:
        if n in one_gene:
            status[n] = {"gene":1}
        elif n in two_genes:
            status[n] = {"gene":2}
        else:
            status[n] = {"gene":0}
        if n in have_trait:
            status[n]["trait"] = True
        else:
            status[n]["trait"] = False
      
    return status  


if __name__ == "__main__":
    main()
