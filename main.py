from typing import Any

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


class Book(BaseModel):
    id: int
    title: str
    author: str
    address: "Address"


class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str


books: list[Book] = []


@app.get("/")
def root():
    return {"message": "Welcome to the Book API!"}


@app.get("/books")
def get_books():
    return books


@app.get("/books/search")
def search_book(query: str):
    result = [
        book
        for book in books
        if query.lower() in book.title.lower() or query.lower() in book.author.lower()
    ]
    return result


@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    return HTTPException(status_code=404, detail="Book not found")


@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(book: Book):
    books.append(book)
    return book


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book.id == book_id:
            deleted_book = books.pop(index)
            return deleted_book
    return {"error": "Book not found"}


@app.get("/test")
def test(query: Any):
    return {"message": f"This is a test endpoint. Query: {query}"}


class UserNotFoundException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(UserNotFoundException)
def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": f"User '{exc.name}' not found."},
    )


@app.get("/users/{name}")
def get_user(name: str):
    if name != "kaushal":
        raise UserNotFoundException(name=name)
    return {"name": "kaushal", "message": "User found!"}
