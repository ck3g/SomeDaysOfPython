from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

import models
from database import engine

from routers import admin, auth, todos, user

app = FastAPI()

# only runs then the database file is not exists
models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(admin.router)
app.include_router(todos.router)


@app.get("/healthy")
def health_check():
    return {"status": "healthy"}


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
