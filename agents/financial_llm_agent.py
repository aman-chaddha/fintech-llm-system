from transformers import pipeline
import sqlite3
from datetime import datetime

# Load lightweight summarization LLM (FLAN-T5-Small)
summarizer = pipeline("summarization", model="google/flan-t5-small")

# Connect to the SQLite DB
conn = sqlite3.connect("fintech_data.db")
cursor = conn.cursor()

# Step 1: Fetch latest news
cursor.execute("SELECT title, summary FROM news ORDER BY id DESC LIMIT 3")
news_items = cursor.fetchall()
news_text = " ".join([f"{title}: {summary}" for title, summary in news_items])

# Step 2: Fetch latest risk data
cursor.execute("SELECT ticker, volatility, var FROM risk ORDER BY timestamp DESC LIMIT 3")
risk_data = cursor.fetchall()
risk_text = " | ".join([f"{ticker} has volatility {vol:.2f} and VaR {var:.2f}" for ticker, vol, var in risk_data])

# Step 3: Combine context
combined_text = f"Market News: {news_text}. Risk Data: {risk_text}"

# Step 4: Summarize using LLM
print("\n🧠 Generating financial insights...\n")
insight = summarizer(combined_text, max_length=150, min_length=30, do_sample=False)

print("📊 Financial Assistant Insight:\n")
print(insight[0]['summary_text'])
