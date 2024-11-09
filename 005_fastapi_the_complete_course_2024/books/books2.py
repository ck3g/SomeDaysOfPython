from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=0, max_length=100)
    rating: int = Field(gt=-1, lt=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "John Doe",
                "description": "Description of the book",
                "rating": 5,
            }
        }
    }


BOOKS = [
    Book(1, "Fluent Python", "Luciano Ramalho", "Fluent description", 5),
    Book(2, "Python testing with pytest", "Brian Okken", "Testing description", 4),
    Book(
        3,
        "Designing Data-Intensive Applications",
        "Martin Kleppmann",
        "Designing description",
        3,
    ),
    Book(4, "Distributed systems", "Van Steen Tanenbaum", "Distributed description", 5),
    Book(5, "Python Crash Course", "Eric Matthes", "Crash description", 4),
    Book(
        6, "The shortest history of Germany", "James Hawes", "Shortest description", 3
    ),
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}")
async def read_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book

    return {}


@app.post("/books")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1

    return book
