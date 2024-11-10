from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field


app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=0, max_length=100)
    rating: int = Field(ge=1, le=5)
    published_date: int = Field(ge=1900, le=2030)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "John Doe",
                "description": "Description of the book",
                "rating": 5,
                "published_date": 2024,
            }
        }
    }


BOOKS = [
    Book(1, "Fluent Python", "Luciano Ramalho", "Fluent description", 5, 2023),
    Book(
        2, "Python testing with pytest", "Brian Okken", "Testing description", 4, 2022
    ),
    Book(
        3,
        "Designing Data-Intensive Applications",
        "Martin Kleppmann",
        "Designing description",
        3,
        2016,
    ),
    Book(
        4,
        "Distributed systems",
        "Van Steen Tanenbaum",
        "Distributed description",
        5,
        2015,
    ),
    Book(5, "Python Crash Course", "Eric Matthes", "Crash description", 4, 2022),
    Book(
        6,
        "The shortest history of Germany",
        "James Hawes",
        "Shortest description",
        3,
        2010,
    ),
]


@app.get("/books")
async def read_all_books(published_date: Optional[int] = Query(None, ge=1900, le=2030)):
    if published_date is None:
        return BOOKS

    books = []
    for book in BOOKS:
        if book.published_date == published_date:
            books.append(book)

    return books


@app.get("/books/{book_id}")
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book

    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/books/")
async def read_book_by_raing(book_rating: int = Query(ge=1, le=5)):
    books = []
    for book in BOOKS:
        if book.rating == book_rating:
            books.append(book)

    return books


@app.post("/books")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


@app.put("/books")
async def update_book(updated_book: BookRequest):
    book_changed = False
    for i, book in enumerate(BOOKS):
        if book.id == updated_book.id:
            BOOKS[i] = updated_book
            book_changed = True

    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/books/{book_id}")
async def delete_book(book_id: int = Path(gt=0)):
    book_deleted = False
    for i, book in enumerate(BOOKS):
        if book.id == book_id:
            BOOKS.pop(i)
            book_deleted = True
            break

    if not book_deleted:
        raise HTTPException(status_code=404, detail="Item not found")


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1

    return book
