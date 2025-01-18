from typing import Annotated

from database import SessionLocal
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from models import Comments
from models import Posts
from pydantic import BaseModel
from pydantic import Field
from routers.auth import get_current_user
from sqlalchemy.orm import Session

router = APIRouter(prefix="/comments", tags=["comments"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class CommentsRequest(BaseModel):
    content: str = Field(min_length=3)


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/create/{post_id}", status_code=status.HTTP_201_CREATED)
async def create_comment(
    user: user_dependency, db: db_dependency, new_comment: CommentsRequest, post_id: int
):
    if user is None:
        raise HTTPException(status=404, detail="User Not Found.")
    comment_model = Comments(
        **new_comment.model_dump(), owner_id=user.get("id"), original_post=post_id
    )
    db.add(comment_model)
    db.commit()
