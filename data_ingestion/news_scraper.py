import requests
from bs4 import BeautifulSoup

def scrape_yahoo_finance_news():
    url = "https://finance.yahoo.com/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Failed to fetch news. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    headlines = soup.select("h3 a")

    news = []
    for headline in headlines:
        title = headline.get_text().strip()
        link = "https://finance.yahoo.com" + headline.get("href")
        news.append((title, link))

    print("\n📢 Top Yahoo Finance News Headlines:\n")
    for i, (title, link) in enumerate(news[:10], 1):
        print(f"{i}. {title}")
        print(f"   🔗 {link}")

if __name__ == "__main__":
    scrape_yahoo_finance_news()
