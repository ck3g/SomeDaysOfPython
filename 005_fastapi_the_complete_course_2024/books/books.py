from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {"title": "Fluent Python", "author": "Luciano Ramalho", "category": "Programming"},
    {
        "title": "Python testing with pytest",
        "author": "Brian Okken",
        "category": "Programming",
    },
    {
        "title": "Designing Data-Intensive Applications",
        "author": "Martin Kleppmann",
        "category": "Programming",
    },
    {
        "title": "Distributed systems",
        "author": "Van Steen Tanenbaum",
        "category": "Programming",
    },
    {
        "title": "Python Crash Course",
        "author": "Eric Matthes",
        "category": "Programming",
    },
    {
        "title": "The shortest history of Germany",
        "author": "James Hawes",
        "category": "History",
    },
]


@app.get("/books")
async def read_all_books(category: str | None = None):
    if category is None:
        return BOOKS

    books = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books.append(book)

    return books


@app.get("/books/{title}")
async def read_book(title: str):
    for book in BOOKS:
        if book["title"].casefold() == title.casefold():
            return book

    return {}
