from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return {"data": "blog list"}


@app.get("/blog/{id}")
def show(id):
    return {"data": {"id": id}}


@app.get("/about")
def about():
    return {"data": {"about": "page"}}
