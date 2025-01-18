from typing import Annotated

from database import SessionLocal
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from models import Posts
from pydantic import BaseModel
from routers.auth import get_current_user
from sqlalchemy.orm import Session

router = APIRouter(prefix="/posts", tags=["posts"])


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


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user_posts(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status=404, detail="User Not Found.")
    return db.query(Posts).filter(Posts.owner_id == user.get("id")).all()


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_post(user: user_dependency, db: db_dependency, new_post: PostRequest):
    if user is None:
        raise HTTPException(status=404, detail="User Not Found.")
    post_model = Posts(
        **new_post.model_dump(), username=user.get("username"), owner_id=user.get("id")
    )
    db.add(post_model)
    db.commit()


@router.delete("/remove/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_post(user: user_dependency, db: db_dependency, post_id: int):
    if user is None:
        raise HTTPException(status=404, detail="User Not Found.")
    db.query(Posts).filter(Posts.id == post_id).filter(
        Posts.owner_id == user.get("id")
    ).delete()
    db.commit()


@router.put("like/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def like_post(user: user_dependency, db: db_dependency, post_id: int):
    if user is None:
        raise HTTPException(status=404, detail="User Not Found.")
    post_to_like = (
        db.query(Posts).filter(Posts.id == post_id).update({"likes": Posts.likes + 1})
    )
    db.commit()
