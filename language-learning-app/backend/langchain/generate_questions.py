import os
from langchain_core.prompts import PromptTemplate
# from langchain.chains.sequential import SequentialChain, SimpleSequentialChain
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers.json import JsonOutputParser
from dotenv import load_dotenv

load_dotenv('.env.local') 

import langchain
langchain.debug = False  # Or True if you want debug mode
langchain.llm_cache = None


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("No OpenAI API key found in environment variables")

# initialize model
llm = ChatOpenAI(api_key=OPENAI_API_KEY, model='gpt-3.5-turbo', temperature=0.5, verbose=False)

# generate a question based on question type 
generate_question_template = PromptTemplate.from_template(
    template="Generate a {difficulty} {question_type} question for a person who is learning {language} in their native language {native_language}."
            "Return the response in JSON format as follows: {{\"question\": \"[question text]\"}}"
)

# fill in the blank answer choice generation
generate_blank_choices_template = PromptTemplate.from_template(
    template="For the question {question} generate four answer choices and ensure there is one clear right answer."
             "Return the response in JSON format as follows: {{\"choices\": [\"A: choice1\", \"B: choice2\", \"C: choice3\", \"D: choice4\"]}}"
    )

# question explanation fill blank
generate_answer_explanation = PromptTemplate.from_template(
    template="For the question {question} and answer choices {generated_answers}, clearly exaplin which answer is correct and why"
             "Return the response in JSON format as follows: {{\"correct_answer\": \"[correct choice]\", \"explanation\": \"[explanation]\"}}"
)

# chains
question_chain = generate_question_template | llm | JsonOutputParser()
answers_fill_blank_chain = generate_blank_choices_template | llm | JsonOutputParser()
explanation_chain = generate_answer_explanation | llm | JsonOutputParser()


def generate_question(inputs: dict):
    question_results = question_chain.invoke(inputs)

    if inputs["question_type"] != "fill_blank":
        return question_results # should be a json with just the question text
    
    else:
        # for fill in the blank
        answers_result = answers_fill_blank_chain.invoke({"question":question_results["question"]})
        explanation_result = explanation_chain.invoke({"question":question_results["question"], "generated_answers":str(answers_result["choices"])})
        
        return {
            "question": question_results["question"],
            "choices": answers_result["choices"],
            "correct_answer": explanation_result["correct_answer"],
            "explanation": explanation_result["explanation"]

        }
       

# inputs = {"question_type":"writing_prompt", 
#         "difficulty":"easy", 
#         "language":"es", 
#         "native_language":"en"}

# question_json = generate_question(inputs=inputs)

# print(question_json)