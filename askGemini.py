import google.generativeai as genai
import json
import ast
import os

# Suppress gRPC logging
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GRPC_ENABLE_FORK_SUPPORT"] = "1"  # This prevents some warnings related to forking


# Configure the API key
genai.configure(api_key="<YOUR_GEMINI_API_KEY")

# Model definition
model = genai.GenerativeModel("gemini-1.5-flash")

# Multiple choice questions as a dictionary
questions = {
    1: {
        "question": "What is the chemical symbol for gold?",
        "options": {
            "A": "Ag",
            "B": "Au",
            "C": "Fe",
            "D": "Pt"
        },
    },
    2: {
        "question": "Which planet is known as the 'Red Planet'?",
        "options": {
            "A": "Venus",
            "B": "Jupiter",
            "C": "Mars",
            "D": "Saturn"
        },
    }
}

# Converts questions dictionry to a string
question_str = json.dumps(questions, indent=4)

# Generates response 
response = model.generate_content(
    "Hello, answer these questions " + question_str + " and return the answer to me in the same format I gave you the questions"
)

# Print the raw response 
print("Raw response:", response.text)

# Extracts answers
try:
    # Assuming the response contains the full answer in a valid Python format
    answers = response.text[8:-5]
    answers = ast.literal_eval(answers)  # Parses to python dictionary
    
    # Prints answers
    print("Formatted Answers:\n", json.dumps(answers, indent=4))
    
except (SyntaxError, ValueError) as e:
    print(f"Error while parsing AI response: {e}")
    answers = None

