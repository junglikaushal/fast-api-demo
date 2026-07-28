import time

import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"message": "Rate limit exceeded. Please try again later."},
    )


cache_data = []
last_fetch_time = 0


@app.get("/news")
@limiter.limit("5/minute")
def get_news(request: Request):
    global cache_data, last_fetch_time
    current_time = time.time()
    # Check if the cache is older than 10 minutes (600 seconds)
    if current_time - last_fetch_time > 600 or not cache_data:
        response = requests.get("https://news.ycombinator.com/")
        soup = BeautifulSoup(response.text, "html.parser")
        cache_data = [item.text for item in soup.find_all("span", class_="titleline")]
        last_fetch_time = current_time
    return {"news": cache_data[:10]}
