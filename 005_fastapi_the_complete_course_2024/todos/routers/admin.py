from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status

from models import Todos
from database import SessionLocal
from .auth import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DBDependency = Annotated[Session, Depends(get_db)]
UserDependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todos", status_code=status.HTTP_200_OK)
async def read_all(user: UserDependency, db: DBDependency):
    if user is None or user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )

    return db.query(Todos).all()


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: UserDependency, db: DBDependency, todo_id: int = Path(gt=0)
):
    if user is None or user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
