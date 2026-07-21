import ast
import difflib
import json
import operator
import os
import random
import re
from datetime import datetime

USER_DATA_FILE = "user_data.json"
HISTORY_LOG_FILE = "chat_history.txt"
DEFAULT_BOT_NAME = "Chatty"

FUZZY_CUTOFF = 0.8
STRICT_FUZZY_CUTOFF = 0.85
EXIT_KEYWORDS = {"exit", "quit", "bye", "goodbye", "farewell", "see you", "later"}

GREETING_KEYWORDS = {
    "hi", "hii", "hiii", "hello", "helo", "hellooo", "hey", "heyy",
    "yo", "sup", "greetings", "good morning", "gud morning",
    "good afternoon", "good evening",
}

THANKS_KEYWORDS = {"thanks", "thank you", "thanx", "thankyou", "thx", "ty"}

COMPLIMENT_KEYWORDS = {
    "smart", "awesome", "amazing", "great", "cool", "brilliant",
    "clever", "genius", "wonderful", "impressive",
}

HELP_KEYWORDS = {"help", "commands", "options", "guide", "what can i ask"}

WEATHER_KEYWORDS = {"weather", "temperature", "forecast", "climate", "rain", "sunny"}

MOTIVATION_KEYWORDS = {"motivate", "motivation", "inspire", "encourage", "demotivated", "pep talk"}

QUOTE_KEYWORDS = {"quote", "quotes", "saying", "wisdom"}

CREATOR_KEYWORDS = {
    "who made you", "who created you", "your creator", "who built you",
    "your developer", "who developed you",
}

CAPABILITY_KEYWORDS = {
    "what can you do", "your features", "your capabilities", "abilities",
    "what do you do",
}

JOKE_KEYWORDS = {"joke", "jokes", "funny", "laugh", "make me laugh"}

FACT_KEYWORDS = {"fact", "facts", "tell me a fact", "random fact"}
TECH_FACT_KEYWORDS = {"tech fact", "technology fact", "computer fact"}
SCIENCE_FACT_KEYWORDS = {"science fact", "scientific fact"}

TIME_KEYWORDS = {"time", "current time", "what time", "clock", "time please"}
DATE_KEYWORDS = {"date", "today's date", "current date", "what date"}
DAY_KEYWORDS = {"what day", "today", "day today"}
MONTH_KEYWORDS = {"month", "current month", "what month"}
YEAR_KEYWORDS = {"year", "current year", "what year"}

COIN_TOSS_KEYWORDS = {"coin toss", "flip a coin", "toss a coin", "heads or tails"}
DICE_ROLL_KEYWORDS = {"roll a dice", "dice roll", "roll dice", "throw a dice"}
RPS_KEYWORDS = {"rock paper scissors", "play rps", "rps"}
GUESS_NUMBER_KEYWORDS = {"guess the number", "number game", "guess my number"}

HISTORY_KEYWORDS = {"history", "show history", "chat history", "conversation history"}
CLEAR_HISTORY_KEYWORDS = {"clear history", "delete history", "reset history"}
CLEAR_MEMORY_KEYWORDS = {"clear memory", "forget me", "reset memory", "forget my name"}

HOW_ARE_YOU_KEYWORDS = {"how are you", "how are you doing", "how's it going"}
BOT_NAME_KEYWORDS = {"what is your name", "your name", "who are you"}
BOT_AGE_KEYWORDS = {"how old are you", "your age"}
FAVORITE_COLOR_KEYWORDS = {"favorite color", "favourite color"}
FAVORITE_FOOD_KEYWORDS = {"favorite food", "favourite food"}

MOOD_WORDS = {
    "fine", "good", "great", "ok", "okay", "alright", "well", "happy",
    "excited", "tired", "sad", "bad", "upset", "angry", "bored", "not good",
    "not well", "not okay", "not great",
}
NEGATIVE_MOODS = {"tired", "sad", "bad", "upset", "angry", "bored"}

RPS_CHOICES = ("rock", "paper", "scissors")

# --- Knowledge base --------------------------------------------------------
# Rule-based "encyclopedia" the bot can recite from when a known topic is
# mentioned. Keys are lowercase topic names.

KNOWLEDGE_BASE = {
    "artificial intelligence": (
        "Artificial Intelligence (AI) is the branch of computer science "
        "focused on building systems that can perform tasks that normally "
        "require human intelligence, such as reasoning and learning."
    ),
    "machine learning": (
        "Machine Learning (ML) is a subset of AI where computers learn "
        "patterns from data instead of being explicitly programmed with rules."
    ),
    "deep learning": (
        "Deep Learning uses multi-layered neural networks to learn complex "
        "patterns from large amounts of data, powering things like image "
        "and speech recognition."
    ),
    "neural networks": (
        "Neural Networks are computing systems loosely inspired by the "
        "human brain, made of layers of interconnected nodes (neurons) "
        "that learn to map inputs to outputs."
    ),
    "nlp": (
        "NLP (Natural Language Processing) is the field that helps "
        "computers understand, interpret, and generate human language."
    ),
    "computer vision": (
        "Computer Vision is the field of AI that enables computers to "
        "interpret and understand visual information from images or video."
    ),
    "data science": (
        "Data Science combines statistics, programming, and domain "
        "knowledge to extract insights and value from data."
    ),
    "python": (
        "Python is a beginner-friendly, high-level programming language "
        "known for its readable syntax and huge ecosystem of libraries."
    ),
    "java": (
        "Java is a widely used, object-oriented programming language "
        "known for its portability thanks to the 'write once, run "
        "anywhere' philosophy of the JVM."
    ),
    "c++": (
        "C++ is a powerful, high-performance programming language that "
        "supports both procedural and object-oriented programming."
    ),
    "oop": (
        "OOP (Object-Oriented Programming) is a programming paradigm "
        "based on the idea of 'objects', which bundle data and behavior "
        "together using classes."
    ),
    "class": (
        "A class is a blueprint for creating objects, defining the "
        "attributes and methods that its objects will have."
    ),
    "object": (
        "An object is a specific instance of a class, containing its own "
        "data (attributes) and behavior (methods)."
    ),
    "function": (
        "A function is a reusable, named block of code that performs a "
        "specific task and can accept inputs and return outputs."
    ),
    "loop": (
        "A loop lets you repeat a block of code multiple times, such as "
        "Python's 'for' and 'while' loops."
    ),
    "dictionary": (
        "A dictionary is a Python data structure that stores data as "
        "key-value pairs for fast lookups by key."
    ),
    "tuple": (
        "A tuple is an ordered, immutable collection of items in Python, "
        "written using parentheses like (1, 2, 3)."
    ),
    "list": (
        "A list is an ordered, mutable collection of items in Python, "
        "written using square brackets like [1, 2, 3]."
    ),
    "set": (
        "A set is an unordered collection of unique items in Python, "
        "useful for removing duplicates and fast membership checks."
    ),
    "regex": (
        "Regex (regular expressions) is a mini-language for matching "
        "patterns in text, used heavily in this very chatbot!"
    ),
    "github": (
        "GitHub is a cloud platform for hosting Git repositories, "
        "enabling collaboration, code review, and version control online."
    ),
    "git": (
        "Git is a distributed version control system that tracks changes "
        "to your code over time, letting you branch, merge, and collaborate."
    ),
}

KNOWLEDGE_SYNONYMS = {
    "ai": "artificial intelligence",
    "ml": "machine learning",
    "dl": "deep learning",
    "nn": "neural networks",
    "cv": "computer vision",
    "ds": "data science",
}


def _build_knowledge_word_map():
    """Map every individual word in each topic (and its synonyms) back
    to the full topic name, enabling per-word fuzzy matching."""
    word_map = {}
    for topic in KNOWLEDGE_BASE:
        for word in topic.split():
            word_map[word] = topic
    for synonym, topic in KNOWLEDGE_SYNONYMS.items():
        word_map[synonym] = topic
    return word_map


KNOWLEDGE_WORD_MAP = _build_knowledge_word_map()
PROGRAMMING_JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "Why don't scientists trust atoms? Because they make up everything!",
    "There are only 10 types of people: those who understand binary and those who don't.",
    "A SQL query walks into a bar, walks up to two tables and asks: 'Can I join you?'",
    "Why do Java developers wear glasses? Because they don't C#.",
    "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
    "I told my computer I needed a break, and it said 'No problem, I'll go to sleep.'",
    "Why did the programmer quit his job? Because he didn't get arrays.",
    "What's a programmer's favorite place to hang out? The Foo Bar.",
    "Why do programmers hate nature? It has too many bugs and no debugger.",
    "In order to understand recursion, you must first understand recursion.",
    "A byte walks into a bar looking miserable. The bartender asks what's wrong. 'Parity error,' says the byte.",
    "Why was the JavaScript developer sad? Because he didn't Node how to Express himself.",
    "There's no place like 127.0.0.1.",
    "Why do programmers always mix up Halloween and Christmas? Because Oct 31 == Dec 25.",
    "!false — it's funny because it's true.",
    "Real programmers count from 0.",
    "Why did the developer go broke? Because he used up all his cache.",
    "To understand what recursion is, you must first understand recursion.",
    "Why was the function sad after a party? It didn't get called.",
    "A programmer's spouse says 'Go to the store and get a loaf of bread. If they have eggs, get a dozen.' The programmer comes home with 12 loaves of bread.",
    "Debugging: being the detective in a crime movie where you are also the murderer.",
    "Why did the programmer bring a ladder to work? To reach the high-level code.",
    "I'd tell you a UDP joke, but you might not get it.",
    "Why do Python programmers wear glasses? Because they can't C.",
    "I would tell you a joke about TCP, but I'd have to keep telling it until you got it.",
    "Why did the array feel useless? Because it had no elements of surprise.",
    "There are two hard problems in computer science: cache invalidation, naming things, and off-by-one errors.",
    "How do you comfort a JavaScript bug? You console it.",
    "Why do programmers prefer using the terminal? Because it's a shell of a good time.",
    "What do you call a programmer from Finland? Nerdic.",
]

MOTIVATIONAL_QUOTES = [
    "Every expert was once a beginner. Keep going!",
    "Small progress every day adds up to big results.",
    "Your only limit is the one you set for yourself.",
    "Discipline beats motivation on the hard days — show up anyway.",
    "Mistakes are proof that you're trying and learning.",
    "Focus on progress, not perfection.",
    "The best time to start was yesterday; the next best time is now.",
]

INSPIRATIONAL_QUOTES = [
    "Great things are built one small, consistent effort at a time.",
    "Believe you can, and you're already halfway there.",
    "Every line of code you write today makes tomorrow's project easier.",
    "Curiosity is the engine of achievement — keep asking questions.",
    "Your future is created by what you do today, not tomorrow.",
]

SUCCESS_QUOTES = [
    "Success is the sum of small efforts repeated day in and day out.",
    "Consistency turns skills into mastery over time.",
    "Those who keep learning keep growing — never stop upgrading yourself.",
    "Failure is simply feedback on the road to success.",
    "Set the goal, break it into steps, and start with step one today.",
]

GENERAL_FACTS = [
    "Honey never spoils — archaeologists have found edible honey in ancient tombs.",
    "A group of flamingos is called a 'flamboyance'.",
    "Bananas are berries, but strawberries technically aren't.",
    "Octopuses have three hearts and blue blood.",
    "The shortest war in recorded history lasted about 38 minutes.",
]

TECH_FACTS = [
    "The first computer 'bug' was an actual moth found in a Harvard Mark II relay in 1947.",
    "Python was named after the comedy show 'Monty Python's Flying Circus', not the snake.",
    "The QWERTY keyboard layout was designed to slow typists down and reduce jams on old typewriters.",
    "The first computer mouse was made of wood.",
    "Git was created by Linus Torvalds, who also created the Linux kernel.",
    "The '@' symbol was used in emails for the first time in 1971.",
    "More than 700 programming languages exist today, but only a handful are widely used.",
]

SCIENCE_FACTS = [
    "Light from the Sun takes about 8 minutes and 20 seconds to reach Earth.",
    "A day on Venus is longer than a year on Venus.",
    "Human DNA is about 99.9% identical from person to person.",
    "There are more possible chess games than atoms in the observable universe.",
    "Water can boil and freeze at the same time at its 'triple point'.",
]

GREETING_RESPONSES = [
    "Hello", "Hi there", "Hey", "Good to see you", "Greetings",
]

CREATOR_RESPONSES = [
    "I was built by a developer learning to create rule-based chatbots in Python!",
    "A Python developer wrote all my rules and patterns by hand — no AI APIs involved.",
]

COMPLIMENT_RESPONSES = [
    "Aww, thank you! You're pretty great yourself.",
    "That's kind of you to say!",
    "You're making my circuits blush!",
]

THANKS_RESPONSES = ["You're welcome!", "Anytime!", "No problem at all!", "Happy to help!"]

HOW_ARE_YOU_RESPONSES = [
    "I'm just a program, but I'm running smoothly! How about you?",
    "Doing great, thanks for asking! How are you feeling today?",
]

POSITIVE_MOOD_RESPONSES = ["Glad to hear that!", "That's wonderful! What can I do for you?"]
NEGATIVE_MOOD_RESPONSES = [
    "I'm sorry to hear that. I hope things get better soon.",
    "That sounds tough. Do you want to talk about it?",
]

FALLBACK_RESPONSES = [
    "I'm not sure I understand. Could you rephrase that?",
    "Interesting... tell me more.",
    "Hmm, I don't have a rule for that yet. Try typing 'help' to see what I can do.",
    "Sorry, I didn't quite get that.",
]

# --- Name-capture patterns --------------------------------------------------

NAME_PATTERNS = [
    re.compile(r"\bmy name is\s+([a-zA-Z]+)", re.IGNORECASE),
    re.compile(r"\byou can call me\s+([a-zA-Z]+)", re.IGNORECASE),
    re.compile(r"\bcall me\s+([a-zA-Z]+)", re.IGNORECASE),
    re.compile(r"\bthis is\s+([a-zA-Z]+)", re.IGNORECASE),
    re.compile(r"\bi'?m\s+([a-zA-Z]+)", re.IGNORECASE),
    re.compile(r"\bi am\s+([a-zA-Z]+)", re.IGNORECASE),
]

MOOD_PATTERN = re.compile(r"\bi(?:'m| am)\s+(not\s+\w+|\w+)", re.IGNORECASE)

# --- Calculator --------------------------------------------------------

MATH_EXPRESSION_PATTERN = re.compile(r"^[\d\s.+\-*/%()]+$")
CALC_PREFIX_PATTERN = re.compile(r"^(calculate|compute|evaluate|what is)\s+(.*)$", re.IGNORECASE)

ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def safe_eval(expression):
    """Safely evaluate a basic arithmetic expression without using eval().

    Only numeric constants and the operators +, -, *, /, %, ** (and unary
    minus) are allowed. Anything else raises a ValueError.
    """
    parsed = ast.parse(expression, mode="eval")
    return _eval_node(parsed.body)


def _eval_node(node):
    """Recursively evaluate a single AST node for the calculator feature."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in ALLOWED_OPERATORS:
            raise ValueError("Operator not allowed.")
        return ALLOWED_OPERATORS[op_type](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in ALLOWED_OPERATORS:
            raise ValueError("Operator not allowed.")
        return ALLOWED_OPERATORS[op_type](_eval_node(node.operand))
    raise ValueError("Invalid or unsafe expression.")


def is_math_expression(text):
    """Return True if the text looks like a pure arithmetic expression."""
    text = text.strip()
    if not text or not MATH_EXPRESSION_PATTERN.match(text):
        return False
    has_digit = any(ch.isdigit() for ch in text)
    has_operator = any(ch in "+-*/%" for ch in text)
    return has_digit and has_operator


def extract_math_expression(text):
    """Return a cleaned-up math expression from text, or None if there
    isn't one. Handles both bare expressions ("5+6") and prefixed ones
    ("calculate 5+6")."""
    stripped = text.strip()
    prefix_match = CALC_PREFIX_PATTERN.match(stripped)
    candidate = prefix_match.group(2) if prefix_match else stripped
    return candidate if is_math_expression(candidate) else None


# --- Generic fuzzy keyword matching ---------------------------------------
#
# Design note: fuzzy matching is deliberately scoped *per intent*, never
# through one big shared vocabulary. Splitting every keyword phrase into
# individual words and pooling them together (e.g. "current", "me", "you")
# causes unrelated intents to collide on common connector words. Instead:
#   1. Exact substring match against each full keyword phrase.
#   2. Fuzzy match of the *entire* input against that intent's own phrases
#      (catches things like "gud morning" vs "good morning").
#   3. Fuzzy match of individual words (length >= 4, to avoid short-word
#      noise) against that intent's *single-word* keywords only.

MIN_FUZZY_WORD_LENGTH = 4


def contains_keyword(text, keywords, cutoff=FUZZY_CUTOFF):
    """Check whether any keyword/phrase is present in text, either as an
    exact substring or as a fuzzy (typo-tolerant) match scoped to this
    specific intent's own keyword list.
    """
    text = text.strip()
    for keyword in keywords:
        if keyword in text:
            return True

    if difflib.get_close_matches(text, keywords, n=1, cutoff=cutoff):
        return True

    single_word_keywords = [kw for kw in keywords if " " not in kw]
    if single_word_keywords:
        for word in text.split():
            if len(word) >= MIN_FUZZY_WORD_LENGTH:
                if difflib.get_close_matches(word, single_word_keywords, n=1, cutoff=cutoff):
                    return True
    return False


def find_knowledge_topic(text):
    """Detect which (if any) knowledge-base topic the text refers to,
    using exact substring matching first, then fuzzy per-word matching."""
    for topic in sorted(KNOWLEDGE_BASE, key=len, reverse=True):
        if topic in text:
            return topic
    for word in text.split():
        if word in KNOWLEDGE_WORD_MAP:
            return KNOWLEDGE_WORD_MAP[word]
    for word in text.split():
        if len(word) >= MIN_FUZZY_WORD_LENGTH:
            matches = difflib.get_close_matches(word, KNOWLEDGE_WORD_MAP.keys(), n=1, cutoff=0.8)
            if matches:
                return KNOWLEDGE_WORD_MAP[matches[0]]
    return None


def rps_result(user_choice):
    """Play one round of Rock, Paper, Scissors against the bot."""
    bot_choice = random.choice(RPS_CHOICES)
    if user_choice == bot_choice:
        outcome = "It's a tie!"
    elif (
        (user_choice == "rock" and bot_choice == "scissors")
        or (user_choice == "paper" and bot_choice == "rock")
        or (user_choice == "scissors" and bot_choice == "paper")
    ):
        outcome = "You win!"
    else:
        outcome = "I win!"
    return f"You chose {user_choice}, I chose {bot_choice}. {outcome}"

class ConversationMemory:
    """Handles loading, saving, and clearing persistent user data (name)."""

    def __init__(self, file_path=USER_DATA_FILE):
        self.file_path = file_path
        self.data = self._load()

    def _load(self):
        """Load user data from disk if the file exists, else return {}."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as data_file:
                    return json.load(data_file)
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def _save(self):
        """Persist the current user data to disk."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as data_file:
                json.dump(self.data, data_file, indent=4)
        except OSError:
            pass

    def get_name(self):
        """Return the stored user name, or None if it hasn't been set."""
        return self.data.get("name")

    def set_name(self, name):
        """Store the user's name and persist it to disk."""
        self.data["name"] = name
        self._save()

    def clear(self):
        """Erase all stored user data (used by the 'clear memory' command)."""
        self.data = {}
        self._save()


class ConversationHistory:
    """Tracks the current session's exchanges and logs them to disk."""

    def __init__(self, log_file=HISTORY_LOG_FILE):
        self.log_file = log_file
        self.session_log = []

    def add(self, user_text, bot_text):
        """Record one exchange in memory and append it to the log file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = (timestamp, user_text, bot_text)
        self.session_log.append(entry)
        self._write_to_file(entry)

    def _write_to_file(self, entry):
        """Append a single exchange to the persistent chat history file."""
        timestamp, user_text, bot_text = entry
        try:
            with open(self.log_file, "a", encoding="utf-8") as log:
                log.write(f"[{timestamp}] You: {user_text}\n")
                log.write(f"[{timestamp}] Bot: {bot_text}\n")
        except OSError:
            pass

    def show(self):
        """Return a formatted string of this session's conversation."""
        if not self.session_log:
            return "There's no conversation history yet in this session."
        lines = []
        for timestamp, user_text, bot_text in self.session_log:
            lines.append(f"[{timestamp}] You: {user_text}")
            lines.append(f"[{timestamp}] Bot: {bot_text}")
        return "\n".join(lines)

    def clear(self):
        """Clear the in-memory session history and truncate the log file."""
        self.session_log = []
        try:
            with open(self.log_file, "w", encoding="utf-8") as log:
                log.write("")
        except OSError:
            pass


class RuleBasedChatbot:
    """A rule-based chatbot that recognizes intents via keyword and
    pattern matching, then dispatches to small handler methods."""

    def __init__(self, bot_name=DEFAULT_BOT_NAME):
        self.bot_name = bot_name
        self.memory = ConversationMemory()
        self.history = ConversationHistory()
        self.user_name = self.memory.get_name()

        # Mini-game state machine: None, "rps", or "guess".
        self.active_game = None
        self.secret_number = None
        self.guess_attempts = 0

    # ----- Small talk & name handling ------------------------------------

    def _extract_name(self, text):
        """Try every name pattern and return a capitalized name, or None."""
        for pattern in NAME_PATTERNS:
            match = pattern.search(text)
            if match:
                candidate = match.group(1)
                if candidate.lower() not in MOOD_WORDS:
                    return candidate.capitalize()
        return None

    def _handle_set_name(self, name):
        """Store the newly learned name in memory and confirm it."""
        self.user_name = name
        self.memory.set_name(name)
        return f"Nice to meet you, {name}! I'll remember your name."

    def _check_mood(self, text):
        """Detect simple 'I'm feeling X' statements and respond warmly."""
        match = MOOD_PATTERN.search(text)
        if not match:
            return None
        mood = match.group(1).lower()
        if mood.startswith("not") or mood in NEGATIVE_MOODS:
            return random.choice(NEGATIVE_MOOD_RESPONSES)
        if mood in MOOD_WORDS:
            return random.choice(POSITIVE_MOOD_RESPONSES)
        return None

    def _handle_greeting(self):
        """Return a personalized greeting if the user's name is known."""
        greeting = random.choice(GREETING_RESPONSES)
        if self.user_name:
            return f"{greeting}, {self.user_name}!"
        return f"{greeting}!"


    def _handle_clear_memory(self):
        """Forget the user's name and clear all persistent memory."""
        self.memory.clear()
        self.user_name = None
        return "Okay, I've forgotten your name and cleared my memory."

    def _handle_clear_history(self):
        """Clear the session history and truncate the log file."""
        self.history.clear()
        return "Conversation history has been cleared."

    def _handle_show_history(self):
        """Return the full conversation history for this session."""
        return self.history.show()

   
    def _handle_calculator(self, expression):
        """Safely evaluate a math expression and format the result."""
        try:
            result = safe_eval(expression)
            return f"{expression.strip()} = {result}"
        except ZeroDivisionError:
            return "I can't divide by zero — that would break the universe (or at least my code)."
        except Exception:
            return "That doesn't look like a valid expression I can calculate."


    def _start_rps(self):
        """Begin a Rock, Paper, Scissors round."""
        self.active_game = "rps"
        return "Let's play Rock, Paper, Scissors! Type rock, paper, or scissors."

    def _handle_rps_turn(self, text):
        """Process the user's move during an active RPS game."""
        for choice in RPS_CHOICES:
            if choice in text:
                self.active_game = None
                return rps_result(choice)
        return "Please choose rock, paper, or scissors (or type 'exit' to quit the game)."

    def _start_guess_number(self):
        """Begin a Guess-the-Number game with a fresh secret number."""
        self.active_game = "guess"
        self.secret_number = random.randint(1, 100)
        self.guess_attempts = 0
        return "I'm thinking of a number between 1 and 100. Try to guess it!"

    def _handle_guess_turn(self, text):
        """Process the user's guess during an active number-guessing game."""
        match = re.search(r"-?\d+", text)
        if not match:
            return "Please type a number to guess (or 'exit' to quit the game)."
        guess = int(match.group())
        self.guess_attempts += 1
        if guess == self.secret_number:
            attempts = self.guess_attempts
            self.active_game = None
            self.secret_number = None
            return f"Correct! The number was {guess}. You got it in {attempts} tries!"
        if guess < self.secret_number:
            return "Higher! Try again."
        return "Lower! Try again."

    def _handle_coin_toss(self):
        """Flip a virtual coin."""
        return f"The coin landed on {random.choice(['Heads', 'Tails'])}!"

    def _handle_dice_roll(self):
        """Roll a virtual six-sided die."""
        return f"You rolled a {random.randint(1, 6)}!"

    # ----- Date & time -------------------------------------------------

    def _handle_time(self):
        """Return the current time."""
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}."

    def _handle_date(self):
        """Return today's full date."""
        return f"Today's date is {datetime.now().strftime('%B %d, %Y')}."

    def _handle_day(self):
        """Return the current day of the week."""
        return f"Today is {datetime.now().strftime('%A')}."

    def _handle_month(self):
        """Return the current month."""
        return f"The current month is {datetime.now().strftime('%B')}."

    def _handle_year(self):
        """Return the current year."""
        return f"The current year is {datetime.now().strftime('%Y')}."

    # ----- Help & capabilities -------------------------------------------

    def _help_text(self):
        """Return the list of things the chatbot can help with."""
        return (
            "Here's what I can do:\n"
            "- Chat: greetings, thanks, compliments, how I'm feeling\n"
            "- Remember your name across sessions\n"
            "- 'history' / 'clear history' / 'clear memory'\n"
            "- Calculator: just type something like 5+6 or 2**10\n"
            "- Knowledge base: ask about Python, AI, Git, OOP, and more\n"
            "- Jokes, motivational quotes, and fun facts\n"
            "- Games: rock paper scissors, guess the number, coin toss, dice roll\n"
            "- Date & time: time, date, day, month, year\n"
            "- Type 'bye', 'exit', or 'quit' anytime to leave"
        )

    def _capabilities_text(self):
        """Return a short summary of the bot's capabilities."""
        return (
            "I'm a rule-based chatbot: I use keyword matching, regex, and "
            "fuzzy text matching to understand you, then answer using "
            "pre-written rules — no external AI services involved."
        )

    # ----- Main dispatch ---------------------------------------------------

    def get_response(self, user_input):
        """Determine the appropriate response for a single line of input."""
        text = user_input.strip()
        lower_text = text.lower()

        # The exit command always works, even mid-game.
        if contains_keyword(lower_text, EXIT_KEYWORDS, STRICT_FUZZY_CUTOFF):
            return "EXIT"

        # Mini-games take over the conversation until finished.
        if self.active_game == "rps":
            return self._handle_rps_turn(lower_text)
        if self.active_game == "guess":
            return self._handle_guess_turn(lower_text)

        # System / memory commands.
        if contains_keyword(lower_text, CLEAR_MEMORY_KEYWORDS, STRICT_FUZZY_CUTOFF):
            return self._handle_clear_memory()
        if contains_keyword(lower_text, CLEAR_HISTORY_KEYWORDS, STRICT_FUZZY_CUTOFF):
            return self._handle_clear_history()
        if contains_keyword(lower_text, HISTORY_KEYWORDS, STRICT_FUZZY_CUTOFF):
            return self._handle_show_history()

        # Mood / feelings before name capture (avoids "I'm fine" -> name="Fine").
        mood_response = self._check_mood(lower_text)
        if mood_response:
            return mood_response

        # Name capture.
        name = self._extract_name(text)
        if name:
            return self._handle_set_name(name)

        # Calculator.
        expression = extract_math_expression(text)
        if expression:
            return self._handle_calculator(expression)

        # Mini-game triggers.
        if contains_keyword(lower_text, RPS_KEYWORDS, STRICT_FUZZY_CUTOFF):
            return self._start_rps()
        if contains_keyword(lower_text, GUESS_NUMBER_KEYWORDS, STRICT_FUZZY_CUTOFF):
            return self._start_guess_number()
        if contains_keyword(lower_text, COIN_TOSS_KEYWORDS, STRICT_FUZZY_CUTOFF):
            return self._handle_coin_toss()
        if contains_keyword(lower_text, DICE_ROLL_KEYWORDS, STRICT_FUZZY_CUTOFF):
            return self._handle_dice_roll()

        # Fun content: facts, jokes, quotes (specific facts before generic,
        # and all of these checked before the knowledge base so a phrase
        # like "science fact" isn't shadowed by the "data science" topic).
        if contains_keyword(lower_text, TECH_FACT_KEYWORDS, STRICT_FUZZY_CUTOFF):
            return random.choice(TECH_FACTS)
        if contains_keyword(lower_text, SCIENCE_FACT_KEYWORDS, STRICT_FUZZY_CUTOFF):
            return random.choice(SCIENCE_FACTS)
        if contains_keyword(lower_text, FACT_KEYWORDS, STRICT_FUZZY_CUTOFF):
            return random.choice(GENERAL_FACTS + TECH_FACTS + SCIENCE_FACTS)
        if contains_keyword(lower_text, JOKE_KEYWORDS, FUZZY_CUTOFF):
            return random.choice(PROGRAMMING_JOKES)
        if contains_keyword(lower_text, MOTIVATION_KEYWORDS, STRICT_FUZZY_CUTOFF):
            return random.choice(MOTIVATIONAL_QUOTES)
        if contains_keyword(lower_text, QUOTE_KEYWORDS, FUZZY_CUTOFF):
            return random.choice(INSPIRATIONAL_QUOTES + SUCCESS_QUOTES)

        # Knowledge base lookups.
        topic = find_knowledge_topic(lower_text)
        if topic:
            return KNOWLEDGE_BASE[topic]

        # Date & time.
        if contains_keyword(lower_text, TIME_KEYWORDS, STRICT_FUZZY_CUTOFF):
            return self._handle_time()
        if contains_keyword(lower_text, DATE_KEYWORDS, STRICT_FUZZY_CUTOFF):
            return self._handle_date()
        if contains_keyword(lower_text, DAY_KEYWORDS, STRICT_FUZZY_CUTOFF):
            return self._handle_day()
        if contains_keyword(lower_text, MONTH_KEYWORDS, STRICT_FUZZY_CUTOFF):
            return self._handle_month()
        if contains_keyword(lower_text, YEAR_KEYWORDS, STRICT_FUZZY_CUTOFF):
            return self._handle_year()

        # Personality & small talk.
        if contains_keyword(lower_text, HOW_ARE_YOU_KEYWORDS, STRICT_FUZZY_CUTOFF):
            return random.choice(HOW_ARE_YOU_RESPONSES)
        if contains_keyword(lower_text, CREATOR_KEYWORDS, STRICT_FUZZY_CUTOFF):
            return random.choice(CREATOR_RESPONSES)
        if contains_keyword(lower_text, BOT_NAME_KEYWORDS, STRICT_FUZZY_CUTOFF):
            return f"My name is {self.bot_name}!"
        if contains_keyword(lower_text, BOT_AGE_KEYWORDS, STRICT_FUZZY_CUTOFF):
            return "I was 'born' the moment my code first ran — so I'm ageless, really!"
        if contains_keyword(lower_text, CAPABILITY_KEYWORDS, STRICT_FUZZY_CUTOFF):
            return self._capabilities_text()
        if contains_keyword(lower_text, FAVORITE_COLOR_KEYWORDS, STRICT_FUZZY_CUTOFF):
            return "I'd say green — like a terminal that just printed no errors."
        if contains_keyword(lower_text, FAVORITE_FOOD_KEYWORDS, STRICT_FUZZY_CUTOFF):
            return "I don't eat, but if I could, I'd try some bytes for breakfast!"
        if contains_keyword(lower_text, COMPLIMENT_KEYWORDS, STRICT_FUZZY_CUTOFF):
            return random.choice(COMPLIMENT_RESPONSES)
        if contains_keyword(lower_text, THANKS_KEYWORDS, FUZZY_CUTOFF):
            return random.choice(THANKS_RESPONSES)
        if contains_keyword(lower_text, WEATHER_KEYWORDS, STRICT_FUZZY_CUTOFF):
            return "I don't have access to live weather data, but I hope it's a nice day outside!"
        if contains_keyword(lower_text, HELP_KEYWORDS, STRICT_FUZZY_CUTOFF):
            return self._help_text()
        if contains_keyword(lower_text, GREETING_KEYWORDS, FUZZY_CUTOFF):
            return self._handle_greeting()

        return random.choice(FALLBACK_RESPONSES)

    # ----- Main loop ---------------------------------------------------

    def chat(self):
        """Run the interactive chat loop in the terminal."""
        print(f"{self.bot_name}: Hello! I'm {self.bot_name}, your rule-based chatbot.")
        if self.user_name:
            print(f"{self.bot_name}: Welcome back, {self.user_name}!")
        print(f"{self.bot_name}: Type 'help' to see what I can do, or 'bye' to exit.\n")

        while True:
            try:
                user_input = input("You: ")
            except (EOFError, KeyboardInterrupt):
                print(f"\n{self.bot_name}: Goodbye!")
                break

            if not user_input.strip():
                continue

            response = self.get_response(user_input)

            if response == "EXIT":
                farewell = f"Goodbye, {self.user_name}!" if self.user_name else "Goodbye!"
                print(f"{self.bot_name}: {farewell}")
                self.history.add(user_input, farewell)
                break

            print(f"{self.bot_name}: {response}")
            self.history.add(user_input, response)


if __name__ == "__main__":
    bot = RuleBasedChatbot(bot_name=DEFAULT_BOT_NAME)
    bot.chat()

