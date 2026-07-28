import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/posts")
def get_posts():
    response = requests.get("https://jsonplaceholder.typicode.com/posts")
    data = response.json()
    return data


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    resposne = requests.get(f"https://jsonplaceholder.typicode.com/posts/{post_id}")

    if resposne.status_code != 200:
        return HTTPException(status_code=resposne.status_code, detail="Post not found")
    data = resposne.json()
    return data
