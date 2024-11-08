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
]


@app.get("/books")
async def read_all_books():
    return BOOKS
