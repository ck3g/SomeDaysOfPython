from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status

from models import Users
from database import SessionLocal
from .auth import get_current_user, bcrypt_context

router = APIRouter(prefix="/user", tags=["user"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DBDependency = Annotated[Session, Depends(get_db)]
UserDependency = Annotated[dict, Depends(get_current_user)]


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
    password_confirmation: str


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: UserDependency, db: DBDependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized"
        )

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    return {
        "id": user_model.id,
        "username": user_model.username,
        "email": user_model.email,
        "first_name": user_model.first_name,
        "last_name": user_model.last_name,
        "role": user_model.role,
        "phone_number": user_model.phone_number,
    }


@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: UserDependency,
    db: DBDependency,
    change_password_request: ChangePasswordRequest,
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized"
        )

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if not bcrypt_context.verify(
        change_password_request.current_password, user_model.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="invalid password",
        )

    if (
        change_password_request.new_password
        != change_password_request.password_confirmation
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="password and password confirmation to not match",
        )

    new_hashed_password = bcrypt_context.hash(change_password_request.new_password)
    user_model.hashed_password = new_hashed_password

    db.add(user_model)
    db.commit()
