import csv
import itertools
import sys

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
    joint_probability(people, {"Harry"}, {"James"}, {"James"})
    return
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

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
    # Initialize a dictionary that contains gene and traits info for every person
    data = {}
    for name in people:
        genes = 1 * (name in one_gene) + 2 * (name in two_genes)
        trait = name in have_trait

        data[name]["genes"] = genes
        data[name]["trait"] = trait

    probabilities = {}
    for name in people:
        mother = people[name]["mother"]
        father = people[name]["father"]
        genes = data[name]["genes"]
        trait = data[name]["trait"]

        # Trait probability
        probabilities[name] = PROBS["trait"][genes][trait]

        # Gene probability if has parents
        if mother:
            """
            0: no one           : (1 - mother gave) * (1 - father gave)
            1: mother or father : mother gave * (1 - father gave) + (1 - mother gave) * father gave
            2: both             : mother gave * father gave
            
            parent[0] gave = 0.01
            parent[1] gave = 0.5 * (1 - mutation)
            parent[2] gave = 1 - mutation
            """
            parentProbs = {}
            for parent in (mother, father):
                parentGenes = data[parent]["genes"]
                parentProbs[parent] = (
                    PROBS["mutation"] if parentGenes == 0 else
                    0.5 * (1 - PROBS["mutation"]) if parentGenes == 1 else
                    1 - PROBS["mutation"]
                )
            gotFromMother = parentProbs[mother]
            gotFromFather = parentProbs[father]

            if genes == 0:
                probabilities[name] += (1 - gotFromMother) * (1 - gotFromFather)
            elif genes == 1:
                probabilities[name] += (
                    gotFromMother) * (1 - gotFromFather) + \
                    (1 - gotFromMother) * gotFromFather
            else:
                probabilities[name] += gotFromMother * gotFromFather
        # Gene probability if no parents
        else:
            probabilities[name] *= PROBS["gene"][genes]
    
    print(probabilities)


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
