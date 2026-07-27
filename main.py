from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Book(BaseModel):
    id: int
    title: str
    author: str


books: List[Book] = []


@app.get("/")
def root():
    return {"message": "Welcome to the Book API!"}


@app.get("/books")
def get_books():
    return books


@app.get("/books/{book_id}")
def get_book(book_id: int):
    for index, book in enumerate(books):
        if book.id == book_id:
            return book
    return {"error": "Book not found"}


@app.post("/books")
def create_book(book: Book):
    books.append(book)
    return book


@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(books):
        if book.id == book_id:
            books[index] = updated_book
            return updated_book
    return {"error": "Book not found"}


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book.id == book_id:
            deleted_book = books.pop(index)
            return deleted_book
    return {"error": "Book not found"}
