from typing import Optional
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return {"data": "blog list"}


@app.get("/blog")
def blogs(limit=10, published: bool = True, sort: Optional[str] = None):
    return {
        "blogs": {
            "limit": limit,
            "published": published,
            "sort": sort,
        },
    }


# should be before /blog/{id} to avoid shadowing this path
@app.get("/blog/unpublished")
def unpublished():
    return {"data": "all unpublished blogs"}


@app.get("/blog/{id}")
def show(id: int):
    return {"data": {"id": id}}


@app.get("/blog/{id}/comments")
def comments(id, limit=10):
    return {"data": {"comments": id, "limit": limit}}


@app.get("/about")
def about():
    return {"data": {"about": "page"}}
