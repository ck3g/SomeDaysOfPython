from fastapi import FastAPI


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
