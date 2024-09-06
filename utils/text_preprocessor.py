import re
import spacy
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")
nlp = spacy.load("en_core_web_sm")

# Function to clean and preprocess text
def clean_text(text):
    text = re.sub(r"\s+", " ", text)  # Remove extra spaces
    text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation
    return text

# Function to remove stopwords
def remove_stopwords(text):
    stop_words = set(stopwords.words("english"))
    words = [word for word in text.split() if word.lower() not in stop_words]
    return " ".join(words)

# Function to lemmatize text
def lemmatize_text(text):
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc])
