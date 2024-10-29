from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return {"data": "blog list"}


# should be before /blog/{id} to avoid shadowing this path
@app.get("/blog/unpublished")
def unpublished():
    return {"data": "all unpublished blogs"}


@app.get("/blog/{id}")
def show(id: int):
    return {"data": {"id": id}}


@app.get("/blog/{id}/comments")
def comments(id):
    return {"data": {"comments": id}}


@app.get("/about")
def about():
    return {"data": {"about": "page"}}
