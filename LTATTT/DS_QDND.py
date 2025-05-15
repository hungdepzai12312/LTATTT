import requests 
from bs4 import BeautifulSoup
url = "https://www.qdnd.vn"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")  # loc lay thong tin
articles = soup.select("h3,h2 > a")[:10]
for article in articles:
    print(article.text.strip())
