import datetime
import random
import re
from typing import Tuple, Union, Callable, List

# Type definition for response source
ResponseSource = Union[List[str], Callable[[], str]]

def get_current_datetime_response() -> str:
    """
    Generates a response showing the current date and time.
    
    Returns:
        str: A formatted string with the current date and time.
    """
    now = datetime.datetime.now()
    date_str = now.strftime("%B %d, %Y")
    time_str = now.strftime("%I:%M %p")
    return f"📅 Today is **{date_str}** and the current time is 🕒 **{time_str}**."

# Predefined rules linking regular expression patterns to responses.
# Each dictionary represents a rule with:
# - 'intent': The purpose of the user input.
# - 'patterns': Regular expression strings to match against user input.
# - 'responses': Either a list of string responses or a function to run.
RULES = [
    {
        "intent": "greeting",
        "patterns": [
            r"\bhi\b",
            r"\bhello\b",
            r"\bhey\b",
            r"\bgreetings\b",
            r"\bsup\b",
            r"\byo\b"
        ],
        "responses": [
            "Hello! 👋 I'm your friendly rule-based chatbot. How can I help you today? 😊",
            "Hi there! 😄 Hope you are having a wonderful day! What's on your mind?",
            "Hey! Nice to meet you. 👋 What can I help you with today?"
        ]
    },
    {
        "intent": "goodbye",
        "patterns": [
            r"\bbye\b",
            r"\bgoodbye\b",
            r"\bexit\b",
            r"\bquit\b",
            r"\bsee you\b"
        ],
        "responses": [
            "Goodbye! 👋 It was nice chatting with you. Have a great day! 😊",
            "Bye! 🚀 Hope to talk to you again soon. Take care!",
            "Farewell! 🌟 Don't hesitate to come back if you have more questions."
        ]
    },
    {
        "intent": "how_are_you",
        "patterns": [
            r"how are you",
            r"how\'s it going",
            r"how do you do",
            r"how are you doing"
        ],
        "responses": [
            "I'm just a bundle of code, but I'm doing fantastic! 💻 How about you? 😊",
            "I'm operating at 100% efficiency! 🤖 Thanks for asking. How are you doing today?",
            "Doing great! Ready to answer your questions. 🚀 Hope you're doing well too!"
        ]
    },
    {
        "intent": "bot_name",
        "patterns": [
            r"what is your name",
            r"who are you",
            r"your name",
            r"what should i call you"
        ],
        "responses": [
            "I am **Aegis**, your rule-based AI assistant! 🤖",
            "My name is **Aegis**! I'm here to answer questions about Python, AI, and CodSoft. 🚀",
            "You can call me **Aegis**! 😊"
        ]
    },
    {
        "intent": "creator",
        "patterns": [
            r"who created you",
            r"who is your creator",
            r"who programmed you",
            r"who made you"
        ],
        "responses": [
            "I was created by an aspiring AI Developer for the CodSoft Internship project! 🎓💻",
            "A developer built me using Python and Streamlit for Task 1 of the CodSoft AI internship. 🛠️🤖"
        ]
    },
    {
        "intent": "capabilities",
        "patterns": [
            r"what can you do",
            r"what are your features",
            r"how can you help me",
            r"capabilities"
        ],
        "responses": [
            "Here is what I can do: 🌟\n"
            "- Answer questions about **Artificial Intelligence** 🤖\n"
            "- Explain concepts in **Python Programming** 🐍\n"
            "- Provide info about the **CodSoft Internship** 💼\n"
            "- Tell you the current **date and time** 📅\n"
            "- Respond to greetings, how are you, and exit commands.\n\n"
            "Just type your question, and I'll do my best to match it to my rules!"
        ]
    },
    {
        "intent": "help",
        "patterns": [
            r"\bhelp\b",
            r"help me",
            r"i need help",
            r"what to type"
        ],
        "responses": [
            "Don't worry! I'm simple to use. 💡 Try asking me things like:\n"
            "- *'What is Artificial Intelligence?'*\n"
            "- *'Why is Python so popular?'*\n"
            "- *'What is CodSoft?'*\n"
            "- *'What is the current time?'*\n"
            "- Or just type *'bye'* when you want to leave. 👋"
        ]
    },
    {
        "intent": "artificial_intelligence",
        "patterns": [
            r"artificial intelligence",
            r"\bai\b",
            r"machine learning",
            r"deep learning",
            r"neural network"
        ],
        "responses": [
            "**Artificial Intelligence (AI)** is a branch of computer science dedicated to building smart machines capable of performing tasks that typically require human intelligence, such as visual perception, speech recognition, decision-making, and translation. 🤖💡",
            "AI is transforming the world! It includes subfields like **Machine Learning** (where algorithms learn from data) and **Deep Learning** (which uses neural networks modeled after the human brain). 🧠🌟",
            "Fascinating topic! AI allows computers to learn and make decisions. Today, it powers self-driving cars, medical diagnostics, search engines, and smart assistants. 🚗🏥"
        ]
    },
    {
        "intent": "python",
        "patterns": [
            r"python",
            r"why python",
            r"python programming"
        ],
        "responses": [
            "**Python** is a high-level, interpreted programming language known for its readability, simplicity, and versatility. 🐍 It is widely used in web development, data science, machine learning, automation, and more!",
            "Python was created by Guido van Rossum and released in 1991. 🚀 Its syntax is clean and readable, making it one of the most popular languages in the world, especially for AI and Machine Learning!",
            "I am written in Python! 🐍 It's a fantastic language because of its rich ecosystem of libraries (like Streamlit, which is rendering this page)."
        ]
    },
    {
        "intent": "codsoft",
        "patterns": [
            r"codsoft",
            r"internship",
            r"codsoft internship"
        ],
        "responses": [
            "**CodSoft** is a vibrant community and platform that offers virtual internships in various domains like Web Development, Android Development, Python Programming, and Artificial Intelligence. 💼🚀",
            "The CodSoft internship program is designed to help students and enthusiasts gain practical experience by working on real-world projects. It is a great way to build your portfolio! 🎓🌟",
            "CodSoft provides students with hands-on projects (like Task 1: this Rule-Based Chatbot!) to enhance their technical skills and prepare them for careers in tech. 💻✨"
        ]
    },
    {
        "intent": "date_time",
        "patterns": [
            r"date",
            r"time",
            r"clock",
            r"what day is it",
            r"what is the time"
        ],
        "responses": get_current_datetime_response
    }
]

# Fallback responses when no pattern is matched
FALLBACK_RESPONSES = [
    "I'm sorry, I don't quite understand that. 😅 Could you try rephrasing? (Or type 'help' to see what I can do!)",
    "Hmm, that's a bit outside my rulebook! 📚 Can you ask me about AI, Python, CodSoft, or the time? 😊",
    "I'm not sure how to answer that. 🤖 I am a rule-based chatbot, so I work best with specific topics like Python, AI, or greetings. Try typing 'help'!",
    "Oops! I couldn't match your input to any of my rules. 🧩 Feel free to ask about the current date/time, Python, or Artificial Intelligence!"
]

def get_chatbot_response(user_input: str) -> Tuple[str, bool]:
    """
    Matches the user's input against the rules and patterns.
    
    Args:
        user_input (str): The raw input text from the user.
        
    Returns:
        Tuple[str, bool]: A tuple containing:
            - response_text (str): The chatbot's response.
            - is_exit (bool): A boolean flag indicating if the input was an exit command.
    """
    # Clean user input (lowercase and strip extra whitespaces)
    cleaned_input = user_input.strip().lower()
    
    # Check if the input is completely empty
    if not cleaned_input:
        return "I can hear you! Feel free to type something. 🤫", False
        
    # Iterate through defined rules
    for rule in RULES:
        for pattern in rule["patterns"]:
            # Perform case-insensitive regex search
            if re.search(pattern, cleaned_input):
                response_source = rule["responses"]
                
                # Check if response is dynamic (callable)
                if callable(response_source):
                    response_text = response_source()
                else:
                    response_text = random.choice(response_source)
                
                # Determine if this rule triggers exit intent
                is_exit = (rule["intent"] == "goodbye")
                return response_text, is_exit
                
    # Fallback to random default responses if no rules matched
    return random.choice(FALLBACK_RESPONSES), False
