# Fluently 
Language learning applications are widely used, but most fail to provide personalized lessons and feedback based on a user’s real-time performance. This project aims to bridge this gap by creating a language learning app that adapts question difficulty dynamically based on user performance in open-ended exercises. The app generates personalized lessons for each user based on their skill level and analyzes user responses using natural language processing (NLP) techniques to provide real-time feedback on grammar, vocabulary, and semantic comprehension.

## How to Install Required Dependencies:
1. Open a terminal window `cd language-learning-app`
2. Run  `cd backend` to access the backend folder
3. Run  `pip install -r requirements.txt` to install required dependencies
4. Run `python -m spacy download en_core_web_md` to install additional required dataset
5. Open another terminal window `cd language-learning-app`
6. Run  `cd app` to access the frontend folder
7. Run  `npm install` to install required dependencies


## How to Run:
1. Open a terminal window `cd language-learning-app`
2. Run `uvicorn backend.app:main --reload` to start the server
3. Open a new terminal window and `cd language-learning-app/app`
4. To start the application, run `npm run dev`

## How to Use:
1. Create a User Account to track learning progress
2. Generate a quick language lesson that will evaluate your responses using NLP techniques 
3. Further your learning!

## Demo: 
https://youtu.be/W9ZlIGC3o_E
   
**Developed By:**  
Maviya Yaseen  
Safa Mohammed  
Sally Qalawi  
  
**Course:** NLP 6320
