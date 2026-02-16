import requests
from bs4 import BeautifulSoup

url = "http://quotes.toscrape.com"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

quotes = soup.find_all("div", class_="quote")

for q in quotes:
    text = q.find("span", class_="text").text.strip()
    author = q.find("small", class_="author").text
    print(text, "-", author)

with open("quotes.txt", "w", encoding="utf-8") as f:
    for q in quotes:
        text = q.find("span", class_="text").text.strip()
        author = q.find("small", class_="author").text.strip()
        f.write(f"{text} - {author}\n")
