import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/news")
def get_news():
    url = "https://indianexpress.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    news_headlines = []
    for headline in soup.find_all("a", class_="topblockNews__sidebarLink"):
        news_headlines.append(headline.text.strip())
    return {"headlines": news_headlines}
