import spacy
#import openai
from openai import Client
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(".env.local") 

nlp = spacy.load("en_core_web_md")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("No OpenAI API key found in environment variables")

client = Client()

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
        return 75
    elif errors == 2:
        return 50
    else:
        return 25

def check_grammar_with_gpt(sentence):
    prompt = f"Evaluate the grammar correctness of the following sentence and return a score on a scale from 0 to 100. If the score is not a 100, return the correct version of the sentence:\n\n'{sentence}\n\n Use the following template for your response:\n\n [Score]->[correct sentence or 'NULL' if score is 100]'"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  
        messages=[{"role": "user", "content": prompt}]
    )
    response_text = response.choices[0].message.content.strip()

    try:
        score, corrected_sentence = response_text.split("->", 1)
        score = int(score.strip())
        score = max(0, min(100, score))
        return score, corrected_sentence.strip() 
    except (ValueError, IndexError):
        return 50, "Error parsing response"
    
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
    final_score = (0.4 * gpt_score) + (0.3 * spacy_score) + (0.3 * similarity_score)
    return int(final_score)

def check_answer(topic: str, user_answer: str) -> bool:
    spacy_score = check_grammar_spacy(user_answer)
    print(f"SpaCy Grammar Score: {spacy_score}")

    gpt_score, corrected_ans = check_grammar_with_gpt(user_answer)
    print(f"GPT Grammar Score: {gpt_score}")

    similarity_score = check_similarity(topic, user_answer)
    print(f"Similarity Score: {similarity_score}")

    final_score = calculate_final_score(spacy_score, gpt_score, similarity_score)
    print(f"Final Score: {final_score}")

    is_correct = final_score >= 88

    return is_correct, corrected_ans

#'''
# Testing 
topic = "Write about food."
user_answer = "I eat food every day. ate dinner outside later today. go chinese restaurant."
is_correct, correct_ans = check_answer(topic, user_answer)

if is_correct:
    print(f"The user's answer is correct and relevant.  {correct_ans}")
else:
    print(f"The user's answer is either off-topic or grammatically incorrect. {correct_ans}")

#
# '''
