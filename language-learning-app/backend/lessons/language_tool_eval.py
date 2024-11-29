import spacy
import language_tool_python

nlp = spacy.load("en_core_web_md")

# grammar checking tool
tool = language_tool_python.LanguageTool("en-US")

def check_answer(topic: str, user_answer: str, similarity_threshold: float = 0.5) -> bool:    
    # check for grammar
    matches = tool.check(user_answer)
    if matches:
        print("Grammar issues detected:")
        for match in matches:
            print(f"- {match.ruleIssueType}: {match.message}")
        return False
    
    # check topic relevance using semantic similarity
    topic_doc = nlp(topic)
    answer_doc = nlp(user_answer)
    similarity = topic_doc.similarity(answer_doc)
    
    print(f"Similarity Score: {similarity:.2f}") 

    return similarity >= similarity_threshold


topic = "dogs"
user_answer = "Dogs are loyal and friendly."
is_correct = check_answer(topic, user_answer)

if is_correct:
    print("The user's answer is relevant and grammatically correct.")
else:
    print("The user's answer is either off-topic or grammatically incorrect.")
