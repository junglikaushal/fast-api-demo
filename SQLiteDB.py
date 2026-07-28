import sqlite3

from fastapi import FastAPI

app = FastAPI()
conn = sqlite3.connect("mydatabase.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     title TEXT NOT NULL,
                     email TEXT NOT NULL,
                     password TEXT NOT NULL)
            """
)

conn.commit()


@app.get("/")
def home():
    return {"message": "SQLite database is connected successfully!"}
