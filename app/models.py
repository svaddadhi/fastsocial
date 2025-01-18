# Social Media APP
#
#
# User profiles and relationships (follow/unfollow)
# Post creation with media support
# Feed generation
# Direct messaging
# Notifications system
# Hashtag functionality


from database import Base
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)

    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    hashed_password = Column(String)


class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    content = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    likes = Column(Integer, default=0)


class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    original_post = Column(Integer, ForeignKey("posts.id"))
    ownder_id = Column(Integer, ForeignKey("users.id"))


class Relationships(Base):
    __tablename__ = "relationships"

    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    following_id = Column(Integer, ForeignKey("users.id"), nullable=False)
