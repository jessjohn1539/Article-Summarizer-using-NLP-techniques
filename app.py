import streamlit as st
from summarizer import summarize_text
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

# Function to fetch and clean the article text from a URL
def fetch_article(url):
    try:
        # Fetch and parse the article using Beautiful Soup
        response = urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        # Extract paragraphs and join them into a single string
        paragraphs = soup.find_all('p')
        article_text = ' '.join([para.get_text() for para in paragraphs])

        # Clean the text by removing extra spaces and unwanted characters
        article_text = re.sub(r'\s+', ' ', article_text).strip()
        return article_text
    except Exception as e:
        st.error(f"Error fetching the article: {e}")
        return ""

# Main function to run the Streamlit app
def main():
    st.title("Automatic Article Summarizer")
    
    # User input for URL and summary length
    url = st.text_input("Enter the URL of the article:")
    summary_length = st.slider("Select summary length (number of sentences):", min_value=1, max_value=10, value=3)

    # Fetch and display the article text
    if url:
        article_text = fetch_article(url)
        if article_text:
            # Display the fetched article length in words
            article_word_count = len(article_text.split())
            st.write(f"**Original Article Length:** {article_word_count} words")
            
            # Generate and display the summary
            summary = summarize_text(article_text, summary_length)
            summary_word_count = len(summary.split())
            
            st.write("### Summary:")
            st.write(summary)
            
            # Display the summary length in words
            st.write(f"**Summary Length:** {summary_word_count} words")

if __name__ == "__main__":
    main()
