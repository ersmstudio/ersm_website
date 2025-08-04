from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)  # ✅ كان مكتوب password فقط
    is_active = Column(Boolean, default=True)
    avatar_url = Column(String, nullable=True)  # ✅ تم إضافته هنا
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    posts = relationship("Post", back_populates="owner")
    comments = relationship("Comment", back_populates="user")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("UserDB", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    post = relationship("Post", back_populates="comments")
    user = relationship("UserDB", back_populates="comments")
