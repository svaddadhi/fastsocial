from typing import Annotated

from database import SessionLocal
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from pydantic import BaseModel
from sqlalchemy import insert
from sqlalchemy.orm import Session

from app.models import Relationships
from app.models import Users
from app.routers.auth import get_current_user

router = APIRouter(prefix="/relationships", tags=["relationships"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class PostRequest(BaseModel):
    content: str


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/follow/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def follow_user(user: user_dependency, db: db_dependency, user_id: int):
    if user is None:
        raise HTTPException(status=404, detail="User Not Found.")
    user_follow_object = Relationships(follower_id=user.get("id"), following_id=user_id)
    db.add(user_follow_object)
    db.commit()


@router.delete("/unfollow/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unfollow_user(user: user_dependency, db: db_dependency, user_id: int):
    if user is None:
        raise HTTPException(status=404, detail="User Not Found.")
    db.query(Relationships).filter(Relationships.following_id == user_id).filter(
        Relationships.follower_id == user.get("id")
    ).delete()
    db.commit()
