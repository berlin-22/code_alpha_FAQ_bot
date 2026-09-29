import re
import nltk

# Download required NLTK data (silent if already present)
for resource in ["punkt", "punkt_tab", "stopwords", "wordnet"]:
    nltk.download(resource, quiet=True)

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Initialize once
_stop_words = set(stopwords.words("english"))
_lemmatizer = WordNetLemmatizer()


def preprocess(text: str) -> str:
    """
    Preprocess text for NLP matching:
    1. Lowercase
    2. Remove punctuation & special characters
    3. Tokenize
    4. Remove stopwords
    5. Lemmatize
    6. Rejoin into a cleaned string

    Args:
        text: Raw input text.

    Returns:
        Cleaned, preprocessed string.
    """
    # Lowercase
    text = text.lower()

    # Remove punctuation and special characters
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    # Tokenize
    tokens = word_tokenize(text)

    # Remove stopwords and lemmatize
    cleaned_tokens = [
        _lemmatizer.lemmatize(token)
        for token in tokens
        if token not in _stop_words and len(token) > 1
    ]

    return " ".join(cleaned_tokens)
