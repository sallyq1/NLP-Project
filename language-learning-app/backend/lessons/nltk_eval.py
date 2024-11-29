import spacy
import nltk
from nltk import CFG

nltk.download('punkt')

nlp = spacy.load("en_core_web_sm")

# Define a simple CFG grammar for checking basic grammatical structure
cfg_grammar = CFG.fromstring("""
    S -> NP VP
    NP -> DT NN | DT JJ NN | PRP | NN
    VP -> VBZ NP | VBZ ADJP | VBP NP | VBP ADJP | VBZ | VBP
    ADJP -> JJ
    DT -> 'the' | 'a' | 'an'
    NN -> 'NN' | 'NNS' | 'PROPN'
    VBZ -> 'VBZ'
    VBP -> 'VBP'
    JJ -> 'JJ'
    PRP -> 'PRP'
""")

def pos_to_cfg_symbol(pos):
    pos_map = {
        "NN": "NN",
        "NNS": "NN",
        "PROPN": "NN",
        "VBZ": "VBZ",
        "VBP": "VBP",
        "JJ": "JJ",
        "DT": "DT",
        "PRP": "PRP",
    }
    return pos_map.get(pos, None)

# Function to validate grammar using CFG
def validate_grammar_cfg(tokens):
    parser = nltk.ChartParser(cfg_grammar)
    try:
        list(parser.parse(tokens))
        return True  # If parsing is successful
    except ValueError:
        return False

# Function to check grammar using spaCy and CFG
def check_sentence_grammar(sentence):
    # Tokenize and lemmatize using spaCy
    doc = nlp(sentence.lower())
    
    # Extract POS tags and map them to CFG symbols
    pos_sequence = []
    has_subject = False
    has_verb = False
    valid_structure = False

    for token in doc:
        cfg_symbol = pos_to_cfg_symbol(token.pos_)
        if cfg_symbol:
            pos_sequence.append(cfg_symbol)
        
        # Check for the existence of subject and verb
        if token.dep_ == "nsubj" and token.head.dep_ == "ROOT":
            has_subject = True
        if token.dep_ == "ROOT" and token.pos_ == "VERB":
            has_verb = True
        if has_subject and has_verb:
            valid_structure = True

    # Validate CFG and check if the sentence has a valid subject-verb structure
    is_valid_cfg = validate_grammar_cfg(pos_sequence)
    is_valid_sentence = is_valid_cfg and valid_structure
    
    print("\nDependency Analysis (spaCy):")
    for token in doc:
        print(f"{token.text} --> {token.pos_} (Dependency: {token.dep_})")
    
    # Return grammatical validity based on CFG rules and POS structure
    if is_valid_sentence and has_subject:
        return f"'{sentence}' is grammatically correct."
    else:
        return f"'{sentence}' is grammatically incorrect."

# Example sentences
sentence1 = "The AI model achieves results."
sentence2 = "The AI results model achieves."  # Incorrect structure

print(check_sentence_grammar(sentence1))
print(check_sentence_grammar(sentence2))
