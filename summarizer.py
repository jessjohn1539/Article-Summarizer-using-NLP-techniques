import nltk
import numpy as np
import networkx as nx
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# Download required resources
nltk.download("punkt_tab")
nltk.download("stopwords")

# Function to preprocess the text and generate sentence vectors
def preprocess_sentences(sentences):
    stop_words = set(stopwords.words("english"))
    sentence_vectors = []

    for sentence in sentences:
        words = word_tokenize(sentence.lower())
        vector = [word for word in words if word not in stop_words and word.isalnum()]
        sentence_vectors.append(vector)

    return sentence_vectors

# Function to create a similarity matrix based on cosine similarity
def build_similarity_matrix(sentences, sentence_vectors):
    # Initialize the similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    # Compute similarity between sentence pairs
    for i, sent1 in enumerate(sentence_vectors):
        for j, sent2 in enumerate(sentence_vectors):
            if i != j:
                # Compute similarity as the ratio of common words over geometric mean
                common_words = set(sent1) & set(sent2)
                similarity = len(common_words) / (np.sqrt(len(sent1)) * np.sqrt(len(sent2)))
                similarity_matrix[i][j] = similarity

    return similarity_matrix

# Main function to summarize text using the TextRank algorithm
def summarize_text(text, num_sentences=3):
    # Tokenize the text into sentences with explicit language
    sentences = sent_tokenize(text, language='english')
    if len(sentences) <= num_sentences:
        return text

    # Preprocess sentences to generate sentence vectors
    sentence_vectors = preprocess_sentences(sentences)

    # Build the similarity matrix for sentences
    similarity_matrix = build_similarity_matrix(sentences, sentence_vectors)

    # Create a graph and apply the TextRank algorithm using PageRank
    graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(graph)

    # Rank sentences based on their scores
    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

    # Extract the top-ranked sentences to form the summary
    summary = " ".join([ranked_sentences[i][1] for i in range(min(num_sentences, len(ranked_sentences)))])
    return summary
