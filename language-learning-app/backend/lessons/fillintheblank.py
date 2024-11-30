from sentence_transformers import SentenceTransformer, util

# Load pre-trained Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def validate_input_in_context(sentence_with_blank, user_input):
    """
    Validates whether the user's input fits contextually into the sentence.

    Args:
        sentence_with_blank (str): The sentence with a blank (e.g., "The ___ is barking loudly.")
        user_input (str): The user's input for the blank.

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
    
    # Determine if the user input fits contextually
    return similarity > 0.6  # Adjust threshold as needed

# Main function to test the implementation
if __name__ == "__main__":
    # Sentence with a blank
    sentence = "Where did ___ go?"
    
    # User inputs to test
    user_inputs = ["dog", "person", "car", "cat"]
    
    # Validate each user input
    for user_input in user_inputs:
        is_valid = validate_input_in_context(sentence, user_input)
        if is_valid:
            print(f'"{user_input}" fits the sentence contextually.')
        else:
            print(f'"{user_input}" does not fit the sentence contextually.')
