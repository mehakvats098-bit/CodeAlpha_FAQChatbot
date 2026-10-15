# College FAQ Chatbot

A Python-based College FAQ Chatbot developed as part of the CodeAlpha AI Internship. It helps students get quick answers to common college-related questions through a simple graphical user interface.

## Features

- College FAQ question-answering system
- TF-IDF and cosine similarity for matching questions
- Text preprocessing using NLTK
- Confidence threshold for handling unknown questions
- User-friendly Tkinter graphical interface
- Suggested questions for quick access
- Conversation history and Clear Chat option
- Automated tests for important FAQ categories

## Technologies Used

- Python
- Tkinter
- NLTK
- Scikit-learn
- TF-IDF Vectorization
- Cosine Similarity
- JSON

## Project Structure

```text
CodeAlpha_FAQChatbot/
├── chatbot.py
├── gui.py
├── faqs.json
├── test_chatbot.py
├── requirements.txt
└── README.md
```

## Installation and Setup

1. Clone or download this repository.
2. Open the project folder in a terminal.
3. Create and activate a virtual environment.

```bash
python -m venv venv
```

On Windows Command Prompt:

```bat
venv\Scripts\activate.bat
```

4. Install the dependencies.

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
python gui.py
```

## Run Automated Tests

```bash
python test_chatbot.py
```

## How It Works

1. The chatbot loads questions, variations, and answers from `faqs.json`.
2. It preprocesses text and converts questions into TF-IDF vectors.
3. Cosine similarity helps identify the closest matching FAQ.
4. A confidence threshold helps the chatbot decide when to return a known answer or an unknown-question response.
5. The Tkinter GUI displays the conversation.

## Limitations

This is a retrieval-based FAQ chatbot, not a generative AI assistant. Its answers depend on the FAQ data provided. College-specific information should be verified using official college sources.

## Internship Project

Developed for the CodeAlpha AI Internship — FAQ Chatbot Task.
