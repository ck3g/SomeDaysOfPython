from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

import models
from database import engine

from routers import admin, auth, todos, user

app = FastAPI()

# only runs then the database file is not exists
models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(admin.router)
app.include_router(todos.router)


@app.get("/healthy")
def health_check():
    return {"status": "healthy"}


@app.get("/")
def home(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)
