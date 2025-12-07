from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.orm import Base


class Member(Base):
    __tablename__ = "member"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    nickname = Column(String(50), nullable=False)
    profile_image = Column(String(255), nullable=True)

    posts = relationship("Post", back_populates="member", cascade="all, delete-orphan")
    liked_posts = relationship("PostLike", back_populates="member", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="member", cascade="all, delete-orphan")
    refresh_tokens = relationship("RefreshToken", back_populates="member", cascade="all, delete-orphan")
