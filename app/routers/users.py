from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from models import Users
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.routers.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user_info(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return db.query(Users).filter(Users.id == user.get("id")).first()
