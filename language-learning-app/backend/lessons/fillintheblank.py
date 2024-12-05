from sentence_transformers import SentenceTransformer, util

# Load pre-trained Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def validate_input_in_context(sentence_with_blank, user_input, valid_examples=None):
    """
    Validates whether the user's input fits contextually into the sentence.

    Args:
        sentence_with_blank (str): The sentence with a blank (e.g., "The ___ is barking loudly.")
        user_input (str): The user's input for the blank.
        valid_examples (list, optional): List of valid contextual examples to compare against.

    Returns:
        bool: True if the input fits the sentence contextually, False otherwise.
    """
    # Fill the blank with the user input
    sentence_filled = sentence_with_blank.replace("___", user_input)
    
    # Generate embeddings for both the original and filled sentences
    embeddings = model.encode([sentence_with_blank.replace("___", "something"), sentence_filled])
    
    # Compute cosine similarity between the embeddings
    similarity = util.cos_sim(embeddings[0], embeddings[1]).item()
    print(f"Sentence similarity: {similarity}")
    
    # If valid examples are provided, check similarity with them
    if valid_examples:
        valid_similarities = [
            util.cos_sim(model.encode([user_input]), model.encode([example])).item()
            for example in valid_examples
        ]
        max_valid_similarity = max(valid_similarities)
        print(f"Max similarity with valid examples: {max_valid_similarity}")
        return similarity > 0.75 and max_valid_similarity > 0.75

    # Default behavior without valid examples
    return similarity > 0.8  

# # Test cases for English sentences
# test_cases = [
#     {
#         "sentence": "The ___ is barking loudly.",
#         "expected_fit": ["dog", "puppy", "hound"],
#         "expected_not_fit": ["car", "book", "chair"]
#     },
#     {
#         "sentence": "The ___ is flying in the sky.",
#         "expected_fit": ["bird", "airplane", "kite"],
#         "expected_not_fit": ["dog", "table", "car"]
#     },
#     {
#         "sentence": "I need a ___ to open this can.",
#         "expected_fit": ["knife", "opener", "tool"],
#         "expected_not_fit": ["chair", "dog", "book"]
#     },
#     {
#         "sentence": "The ___ drove through the city quickly.",
#         "expected_fit": ["car", "truck", "bus"],
#         "expected_not_fit": ["dog", "bird", "knife"]
#     },
# ]

# # Main function to test all cases
# if __name__ == "__main__":
#     for case in test_cases:
#         print(f"\nTesting sentence: {case['sentence']}")
#         for word in case["expected_fit"]:
#             result = validate_input_in_context(case["sentence"], word, case["expected_fit"])
#             print(f'"{word}" - Expected to fit: {"Correct" if result else "Incorrect"}')
#         for word in case["expected_not_fit"]:
#             result = validate_input_in_context(case["sentence"], word, case["expected_fit"])
#             print(f'"{word}" - Expected NOT to fit: {"Correct" if not result else "Incorrect"}')
