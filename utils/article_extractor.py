import requests
from bs4 import BeautifulSoup

# Function to extract the article content from a given URL
def extract_article(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Extract text from common article tags
            paragraphs = soup.find_all("p")
            article_text = " ".join([para.get_text() for para in paragraphs])
            return article_text.strip()
        else:
            return None
    except Exception as e:
        print(f"Error extracting article: {e}")
        return None
