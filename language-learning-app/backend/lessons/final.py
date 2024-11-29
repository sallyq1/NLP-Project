import spacy
import openai
import os
from dotenv import load_dotenv

load_dotenv('.env.local') 

nlp = spacy.load("en_core_web_sm")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("No OpenAI API key found in environment variables")


def check_grammar_spacy(user_answer: str) -> int:
    doc = nlp(user_answer)
    errors = 0

    # Check for subject-verb presence
    has_subject = any(token.dep_ in ("nsubj", "nsubjpass") for token in doc)
    has_verb = any(token.pos_ == "VERB" for token in doc)

    excessive_punct = len([t for t in doc if t.is_punct]) > 3

    if not has_subject:
        errors += 1
        print("No subject found in the sentence.")
    if not has_verb:
        errors += 1
        print("No verb found in the sentence.")
    if excessive_punct:
        errors += 1
        print("Excessive punctuations found in the sentence.")

    if errors == 0:
        return 100
    elif errors == 1:
        return 85
    elif errors == 2:
        return 70
    else:
        return 50

def check_grammar_with_gpt(sentence):
    prompt = f"Evaluate the grammar correctness of the following sentence on a scale from 0 to 100:\n\n'{user_answer}'"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=[{"role": "user", "content": prompt}]
    )
    try:
        score = int(response.choices[0].message["content"].strip())
        return max(0, min(100, score)) 
    except ValueError:
        return 50 
    
def check_similarity(topic: str, user_answer: str) -> int:
    topic_doc = nlp(topic)
    answer_doc = nlp(user_answer)
    similarity = topic_doc.similarity(answer_doc)
    return int(similarity * 100)

def calculate_final_score(spacy_score: int, gpt_score: int, similarity_score: int) -> int:
    """
    Calculate the final score based on weights:
    - GPT Grammar Check: 50%
    - SpaCy Grammar Check: 30%
    - Similarity Check: 20%
    """
    final_score = (0.5 * gpt_score) + (0.3 * spacy_score) + (0.2 * similarity_score)
    return int(final_score)

def check_answer(topic: str, user_answer: str) -> bool:
    spacy_score = check_grammar_spacy(user_answer)
    print(f"SpaCy Grammar Score: {spacy_score}")

    gpt_score = check_grammar_with_gpt(user_answer)
    print(f"GPT Grammar Score: {gpt_score}")

    similarity_score = check_similarity(topic, user_answer)
    print(f"Similarity Score: {similarity_score}")

    final_score = calculate_final_score(spacy_score, gpt_score, similarity_score)
    print(f"Final Score: {final_score}")

    return final_score >= 70


# Testing 
topic = "cat"
user_answer = "The cat climbed the tree near the road."
is_correct = check_answer(topic, user_answer)

if is_correct:
    print("The user's answer is correct and relevant.")
else:
    print("The user's answer is either off-topic or grammatically incorrect.")
