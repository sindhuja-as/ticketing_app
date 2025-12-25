# src/data/preprocess.py

import re
import nltk
import spacy
from nltk.corpus import stopwords

# Download once
nltk.download("stopwords")

# Load resources
STOP_WORDS = set(stopwords.words("english"))
nlp = spacy.load("en_core_web_sm")


def remove_html(text: str) -> str:
    """Remove HTML tags from text"""
    return re.sub(r"<.*?>", " ", text)


def remove_punctuation(text: str) -> str:
    """Remove punctuation and special characters"""
    return re.sub(r"[^a-zA-Z\s]", " ", text)


def clean_text(text: str) -> str:
    """
    Full text cleaning pipeline:
    1. Remove HTML
    2. Lowercase
    3. Remove punctuation
    4. Remove stopwords
    5. Lemmatize
    """
    # Remove HTML
    text = remove_html(text)

    # Lowercase
    text = text.lower()

    # Remove punctuation
    text = remove_punctuation(text)

    # Lemmatization + stopword removal
    doc = nlp(text)
    tokens = [
        token.lemma_
        for token in doc
        if token.text not in STOP_WORDS and not token.is_space
    ]

    return " ".join(tokens)

