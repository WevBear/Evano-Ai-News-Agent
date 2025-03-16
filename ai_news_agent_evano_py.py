import requests
import feedparser
import openai
from bs4 import BeautifulSoup
import time

# OpenAI API Key (replace with your key)
OPENAI_API_KEY = "your-api-key"

# Yahoo Finance RSS Feed URL
RSS_FEED_URL = "https://finance.yahoo.com/rss"

# Function to fetch and parse RSS feed
def fetch_news():
    feed = feedparser.parse(RSS_FEED_URL)
    articles = []
    for entry in feed.entries[:5]:  # Limit to 5 articles per run
        articles.append({
            "title": entry.title,
            "link": entry.link
        })
    return articles

# Function to extract article content
def extract_content(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Finding the article content (Yahoo structure varies, may need tweaking)
    paragraphs = soup.find_all("p")
    article_text = " ".join([p.get_text() for p in paragraphs])
    return article_text[:3000]  # Limit characters to avoid API limit

# Function to summarize article with GPT-4
def summarize_article(article_text):
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Summarize this financial news article in 3 bullet points."},
            {"role": "user", "content": article_text}
        ]
    )
    return response["choices"][0]["message"]["content"]

# Main function to run AI agent
def run_agent():
    news_articles = fetch_news()
    for article in news_articles:
        print(f"Fetching: {article['title']}")
        content = extract_content(article['link'])
        if content:
            summary = summarize_article(content)
            print(f"\nSummary:\n{summary}\n")
            # Store or post summary (can be saved to Firebase, database, etc.)
        time.sleep(2)  # Delay to avoid hitting API limits

if __name__ == "__main__":
    run_agent()
