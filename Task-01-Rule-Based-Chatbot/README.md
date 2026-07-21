# Task 1 - Rule-Based Chatbot

# 🤖 Rule-Based Chatbot

A fully rule-based conversational chatbot built in pure Python — no machine learning, no external AI APIs. It understands user intent through keyword matching, regular expressions, and typo-tolerant fuzzy matching, then responds using hand-written rules.

This project was built as my first internship task to demonstrate core Python concepts: OOP, regex, file I/O, and basic conversational logic.


## Table of Contents

- [Short Description](#short-description)
- [Features](#features)
- [Demo](#demo)
- [Screenshots](#screenshots)
- [Tech Stack](#tech-stack)
- [Project Architecture](#project-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Machine Learning Details](#machine-learning-details)
- [Dataset Information](#dataset-information)
- [Configuration](#configuration)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)
- [Acknowledgements](#acknowledgements)
- [Contact](#contact)

---

## Short Description

`chatbot.py` is a command-line chatbot that simulates natural conversation using **rule-based logic**. It recognizes intents (greetings, questions, commands, small talk) through pattern matching and keyword detection, and responds with pre-written, context-aware replies. It also remembers the user's name across sessions, logs conversation history, and includes small interactive extras like a calculator and mini-games.

---

## Features

- 🧠 **Smart intent matching** — combines exact keyword matching with `difflib` fuzzy matching, so typos like `helo`, `pyhton`, or `gud morning` are still understood
- 💾 **Persistent memory** — remembers the user's name across sessions (`user_data.json`) and greets them back on return
- 📜 **Conversation history** — logs every exchange to `chat_history.txt`; supports `history`, `clear history`, and `clear memory` commands
- ➗ **Safe calculator** — evaluates expressions like `5+6`, `2**10`, `50%4` using Python's `ast` module (no unsafe `eval`)
- 📚 **Built-in knowledge base** — short explanations for AI, Machine Learning, Deep Learning, Neural Networks, NLP, Computer Vision, Data Science, Python, Java, C++, OOP, and core programming concepts (class, object, function, loop, list, tuple, set, dictionary, regex, Git, GitHub)
- 😂 **Fun content** — 30+ programming jokes, motivational/inspirational/success quotes, and tech & science facts
- 🎮 **Mini-games** — Rock-Paper-Scissors, Guess-the-Number, coin toss, and dice roll
- 🕒 **Date & time utilities** — current time, date, day, month, and year
- 🙂 **Personality responses** — answers questions like "who made you," "how old are you," and casual mood check-ins

---

## Demo

Run the script and start chatting in your terminal:

```
Chatty: Hello! I'm Chatty, your rule-based chatbot.
Chatty: Type 'help' to see what I can do, or 'bye' to exit.

You: hi
Chatty: Hi there!
You: my name is Alex
Chatty: Nice to meet you, Alex! I'll remember your name.
You: what is python
Chatty: Python is a beginner-friendly, high-level programming language known for its readable syntax and huge ecosystem of libraries.
You: 5+6
Chatty: 5+6 = 11
You: tell me a joke
Chatty: Why do programmers prefer dark mode? Because light attracts bugs.
You: bye
Chatty: Goodbye, Alex!
```


---

## Tech Stack

- **Language:** Python 3.12+
- **Standard library modules only:**
  - `re` — pattern matching
  - `difflib` — typo-tolerant fuzzy matching
  - `ast` / `operator` — safe expression evaluation for the calculator
  - `json` — persistent user memory
  - `random` — jokes, quotes, facts, and games
  - `datetime` — date/time features
  - `os` — file existence checks

No third-party packages or external APIs are required.

---

## Project Architecture

The chatbot follows a simple, modular, object-oriented design:

```
User Input
    │
    ▼
RuleBasedChatbot.get_response()
    │
    ├── Exit check
    ├── Active mini-game handling (RPS / Guess the Number)
    ├── Memory & history commands
    ├── Mood detection
    ├── Name capture
    ├── Calculator detection
    ├── Mini-game triggers
    ├── Fun content (facts, jokes, quotes)
    ├── Knowledge base lookup
    ├── Date & time
    ├── Personality & small talk
    └── Fallback response
    │
    ▼
ConversationHistory.add()  →  chat_history.txt
ConversationMemory.set_name() → user_data.json
```

Two supporting classes handle persistence:

- **`ConversationMemory`** — loads/saves the user's name to `user_data.json`
- **`ConversationHistory`** — tracks the session's exchanges and appends them to `chat_history.txt`

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/<nooraafra1704-hue>/<CODSOFT>.git
   cd <CODSOFT>
   ```

2. **Check your Python version** (3.12+ recommended, no external dependencies to install)
   ```bash
   python --version
   ```

That's it — no `pip install` needed since the project only uses Python's standard library.

---

## Usage

Run the chatbot from your terminal:

```bash
python chatbot.py
```

Then simply start typing. A few things to try:

| Try typing...              | What happens                          |
|-----------------------------|----------------------------------------|
| `my name is <your name>`    | The bot remembers your name            |
| `what is machine learning`  | Get a knowledge-base explanation       |
| `5 + 6 * 2`                 | Get a calculated result                |
| `tell me a joke`            | Get a random programming joke          |
| `play rock paper scissors`  | Start a mini-game                      |
| `guess the number`          | Start a number-guessing game           |
| `history`                   | View this session's conversation       |
| `clear memory`              | Forget your saved name                 |
| `help`                      | See a full list of supported commands  |
| `bye` / `exit` / `quit`     | End the conversation                   |

---

## Project Structure

```
.
├── chatbot.py          # Main chatbot script (all logic lives here)
├── user_data.json       # Auto-generated: stores the remembered user name
├── chat_history.txt      # Auto-generated: persistent log of all conversations
└── README.md            # Project documentation
```

> `user_data.json` and `chat_history.txt` are created automatically the first time you run the bot — you don't need to create them manually.

---

## API Documentation

Not applicable — this is a standalone command-line script with no exposed API endpoints.

---

## Machine Learning Details

Not applicable. This chatbot is intentionally **100% rule-based**: it uses regular expressions, keyword lists, and `difflib` fuzzy string matching — no models, no training, and no external AI services.

---

## Dataset Information

Not applicable — there is no training dataset. Responses (jokes, quotes, facts, knowledge-base entries) are hand-written and stored directly in the script as Python lists/dictionaries.

---

## Configuration

No environment variables or config files are required. Optional customization points inside `chatbot.py`:

| Constant | Purpose |
|---|---|
| `DEFAULT_BOT_NAME` | Change the bot's display name |
| `USER_DATA_FILE` | Path to the file storing the remembered name |
| `HISTORY_LOG_FILE` | Path to the persistent chat log |
| `FUZZY_CUTOFF` / `STRICT_FUZZY_CUTOFF` | Adjust how forgiving typo matching is |

---

## Roadmap

- [ ] Add a simple GUI (Tkinter) or web front-end
- [ ] Support multi-turn context for more natural conversations
- [ ] Add more knowledge-base topics
- [ ] Export conversation history as PDF/CSV
- [ ] Add unit tests with `pytest`



## Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "Add your feature"`)
4. Push to your branch (`git push origin feature/your-feature`)
5. Open a Pull Request


## License

This project is licensed under the [MIT License](LICENSE) — feel free to use, modify, and distribute it.


## Author

Noor Aafra R
Internship Project — [CodSoft]



## Acknowledgements

- Built as part of an internship task to practice Python fundamentals, OOP, and rule-based logic
- Inspired by classic rule-based chatbot tutorials and pattern-matching techniques



## Contact

- GitHub: [@nooraafra1704-hue](https://github.com/nooraafra1704-hue)
- Email: nooraafra1704@gmail.com
- LinkedIn: [Noor Aafra R](https://linkedin.com/in/NoorAafraR)
