import asyncio
import time

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def home():
    print("Start processing request...")
    await asyncio.sleep(5)
    print("Finished processing request.")
    return {"message": "Hello, World!"}
