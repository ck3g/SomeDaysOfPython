from fastapi import FastAPI

from .schema import Blog

app = FastAPI()


@app.post("/blog")
def create(request: Blog):
    return {"title": request.title, "body": request.body}
