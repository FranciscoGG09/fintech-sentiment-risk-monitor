import requests
from bs4 import BeautifulSoup

url = "https://finance.yahoo.com/news/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all('a')
print(f"Total links found: {len(links)}")

news_count = 0
for a in links:
    title = a.text.strip()
    link = a.get('href', '')
    
    if len(title) > 30:
        if '/article' in link or '/news/' in link:
            news_count += 1
            print(f"[{len(title)}] Title: {title[:50]}... | Link: {link[:50]}...")

print(f"Total over 30 chars: {news_count}")
