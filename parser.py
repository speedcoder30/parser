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
    S -> NP VP | NP VP CP
    
    CP -> Conj NP VP | Conj VP NP
    AJP -> Adj | Adj Adj |Adj Adj Adj | Adj ADP
    ADP -> Adv| VP Adv
    NP -> N | Det N | Det AJP NP | Det N PP| N PP | Det NP Adv
    PP -> P NP
    VP -> V | V NP | V PP | VP Adv | Adv VP
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

    parsed_sentence_list=nltk.tokenize.word_tokenize(sentence.lower())
    alpha_output=[c for c in parsed_sentence_list if c.isalpha()]
    print(alpha_output)
    return alpha_output


def np_chunk(tree:nltk.Tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    noun_phrase_list=list()
    for subtree in tree.subtrees(filter=lambda t: t.label()=="NP"):
        if not find_np_exists(subtree):
            noun_phrase_list.append(subtree)
    return noun_phrase_list

def find_np_exists(np_tree):
    np_exists=False
    for subTree in np_tree:
        try:
            if subTree.label()=="NP":
                return True
            else:
               output= find_np_exists(subTree)
               if output:
                return output
        except:
            error="End of flow"
    return np_exists
if __name__ == "__main__":
    main()
