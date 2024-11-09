from fastapi import Body, FastAPI

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


@app.post("/books")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put("/books")
async def update_book(updated_book=Body()):
    for i, book in enumerate(BOOKS):
        if book.get("title").casefold() == updated_book.get("title").casefold():
            BOOKS[i] = updated_book

    return updated_book


@app.delete("/books/{title}")
async def delete_book(title: str):
    for i, book in enumerate(BOOKS):
        if book.get("title").casefold() == title.casefold():
            BOOKS.pop(i)
            break
