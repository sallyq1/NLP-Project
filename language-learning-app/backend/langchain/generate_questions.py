import os
from fastapi.concurrency import run_in_threadpool
from langchain_core.prompts import PromptTemplate
# from langchain.chains.sequential import SequentialChain, SimpleSequentialChain
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers.json import JsonOutputParser
from dotenv import load_dotenv

load_dotenv('.env.local') 

import langchain
langchain.debug = False  
langchain.llm_cache = None


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("No OpenAI API key found in environment variables")

# initialize model
llm = ChatOpenAI(api_key=OPENAI_API_KEY, model='gpt-3.5-turbo', temperature=0.7, verbose=False)

# generate a question based on question type 
generate_question_template = PromptTemplate.from_template(
    template="Generate a {difficulty} {question_type} language learning question for {language}. "
             "Ensure the question is clear, engaging, and appropriate for language learners. "
             "Include context if relevant. "
             "Return a JSON with: {{\"question\": \"[precise question text]\"}}"
)
# generate_question_template = PromptTemplate.from_template(
#     template="Generate a {difficulty} {question_type} question for a person who is learning {language} in their native language {native_language}."
#             "Return the response in JSON format as follows: {{\"question\": \"[question text]\"}}"
# )

generate_fill_blank_template = PromptTemplate.from_template(
    template="For a language learning question: '{question}', do the following in a single comprehensive response:\n"
             "1. Generate four plausible answer choices\n"
             "2. Clearly identify the correct answer\n"
             "3. Provide a brief, educational explanation\n"
             "Return in JSON format: {{\"question\": str, \"choices\": [str], \"correct_answer\": str, \"explanation\": str}}"
)

multi_question_template = PromptTemplate.from_template(
            "Generate language learning questions for {language} at {difficulty} level:\n\n"
            "Generate 2 unique fill-in-the-blank questions and 2 unique writing prompt questions.\n\n"
            "For each fill-in-the-blank question:\n"
            "- Provide the question text\n"
            "- Use 3 underscores to make the blank like ___\n"
            "- Generate 4 answer choices and ensure there is one clear right answer\n"
            "- Identify the correct answer\n"
            "- Write a explanation to clearly explain which answer is correct and why\n\n"
            "For each writing prompt question:\n"
            "- Create an engaging, context-rich question\n\n"
            "Return in this JSON format:\n"
            "{{\"fill_blank_questions\": ["
            "{{\"question\": \"string\", \"choices\": [\"string\", \"string\", \"string\", \"string\"], \"correct_answer\": \"string\", \"explanation\": \"string\"}},"
            "{{\"question\": \"string\", \"choices\": [\"string\", \"string\", \"string\", \"string\"], \"correct_answer\": \"string\", \"explanation\": \"string\"}}"
            "], "
            "\"writing_prompt_questions\": ["
            "{{\"question\": \"string\"}},"
            "{{\"question\": \"string\"}}"
            "]}}"
)

# # fill in the blank answer choice generation
# generate_blank_choices_template = PromptTemplate.from_template(
#     template="For the question {question} generate four answer choices and ensure there is one clear right answer."
#              "Return the response in JSON format as follows: {{\"choices\": [\"choice1\", \"choice2\", \"choice3\", \"choice4\"]}}"
#     )

# # question explanation fill blank
# generate_answer_explanation = PromptTemplate.from_template(
#     template="For the question {question} and answer choices {generated_answers}, clearly exaplin which answer is correct and why"
#              "Return the response in JSON format as follows: {{\"correct_answer\": \"[correct choice]\", \"explanation\": \"[explanation]\"}}"
# )

# chains
multi_question_chain = multi_question_template | llm | JsonOutputParser()
question_chain = generate_question_template | llm | JsonOutputParser()
fill_blank_chain = generate_fill_blank_template | llm | JsonOutputParser()
# fill_blank_chain = generate_blank_choices_template | llm | JsonOutputParser()
# explanation_chain = generate_answer_explanation | llm | JsonOutputParser()

def generate_question(inputs: dict):
    question_data = multi_question_chain.invoke(input=inputs)

    return question_data
       
# inputs = {
#         "difficulty":"easy", 
#         "language":"en" }

# question_json = generate_question(inputs=inputs)

# print(question_json)