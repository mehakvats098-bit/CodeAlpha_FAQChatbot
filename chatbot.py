
import json
import re
from pathlib import Path

import nltk
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Download stopwords on first use.
try:
    nltk.download("stopwords", quiet=True)
    from nltk.corpus import stopwords
    STOP_WORDS = set(stopwords.words("english"))
except Exception:
    # Fallback if NLTK data cannot be downloaded.
    STOP_WORDS = {
        "a", "an", "the", "is", "are", "am", "do", "does",
        "did", "how", "what", "when", "where", "who", "can",
        "i", "me", "my", "to", "for", "of", "in", "on",
        "and", "or", "please", "tell", "about"
    }

STEMMER = PorterStemmer()
FAQ_FILE = Path(__file__).with_name("faqs.json")

# Similarity threshold: tune this after testing your own questions.
CONFIDENCE_THRESHOLD = 0.22


def preprocess(text):
    """Normalize and stem text for FAQ matching."""
    text = text.lower().replace("'", "")
    words = re.findall(r"[a-z]+", text)

    cleaned = [
        STEMMER.stem(word)
        for word in words
        if word not in STOP_WORDS or word in {"not", "no"}
    ]

    return " ".join(cleaned)


with open(FAQ_FILE, "r", encoding="utf-8") as file:
    faqs = json.load(file)


# Map every alternative phrasing back to its original FAQ.
training_texts = []
faq_indices = []

for index, faq in enumerate(faqs):
    variants = [faq["question"]] + faq.get("variations", [])

    for variant in variants:
        processed = preprocess(variant)

        if processed:
            training_texts.append(processed)
            faq_indices.append(index)


vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    sublinear_tf=True,
    strip_accents="unicode"
)

faq_vectors = vectorizer.fit_transform(training_texts)


GREETINGS = {
    "hi", "hello", "hey", "good morning",
    "good afternoon", "good evening"
}

THANKS = {
    "thanks", "thank you", "thank you so much",
    "thanks a lot"
}


def get_response(user_question):
    """Return a response dictionary for the graphical interface."""

    question = user_question.strip().lower()
    normalized = re.sub(r"[^\w\s']", "", question).strip()

    if not normalized:
        return {
            "answer": "Please type a question so I can help you.",
            "confidence": 0.0,
            "matched_question": None,
            "known": False
        }

    # Simple conversational handling.
    if normalized in GREETINGS:
        return {
            "answer": (
                "Hello! Welcome to the College FAQ Assistant. "
                "I can help with admissions, fees, exams, scholarships, "
                "hostels, placements, and other college-related questions."
            ),
            "confidence": 1.0,
            "matched_question": None,
            "known": True
        }

    if normalized in THANKS:
        return {
            "answer": "You're welcome! Feel free to ask another college-related question.",
            "confidence": 1.0,
            "matched_question": None,
            "known": True
        }

    if normalized in {"bye", "goodbye", "see you"}:
        return {
            "answer": "Goodbye! Best wishes for your studies.",
            "confidence": 1.0,
            "matched_question": None,
            "known": True
        }

    processed = preprocess(user_question)

    if not processed or not vectorizer.vocabulary_:
        return {
            "answer": (
                "I couldn't understand that question. "
                "Try asking about admissions, fees, exams, or scholarships."
            ),
            "confidence": 0.0,
            "matched_question": None,
            "known": False
        }

    user_vector = vectorizer.transform([processed])

    if user_vector.nnz == 0:
        best_score = 0.0
        best_index = 0
    else:
        scores = cosine_similarity(user_vector, faq_vectors).ravel()
        best_position = int(scores.argmax())
        best_score = float(scores[best_position])
        best_index = faq_indices[best_position]

    if best_score < CONFIDENCE_THRESHOLD:
        return {
            "answer": (
                "I'm not confident enough to answer that accurately yet. "
                "Try rephrasing your question or choosing one of the suggested "
                "topics. For official information, please contact your college."
            ),
            "confidence": best_score,
            "matched_question": None,
            "known": False
        }

    return {
        "answer": faqs[best_index]["answer"],
        "confidence": best_score,
        "matched_question": faqs[best_index]["question"],
        "known": True
    }


def main():
    """Optional terminal interface."""
    print("College FAQ Assistant")
    print("Type 'exit' to quit.")

    while True:
        question = input("\nYou: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Bot: Goodbye!")
            break

        result = get_response(question)
        print("Bot:", result["answer"])


if __name__ == "__main__":
    main()
