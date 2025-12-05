import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database.orm import Base


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), nullable=False, index=True)
    content = Column(Text, nullable=False)
    article_image = Column(String(100), nullable=True)

    member_id = Column(Integer, ForeignKey("member.id"), nullable=False, index=True)
    view_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    member = relationship("Member", back_populates="posts")
    likes = relationship("PostLike", back_populates="post", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Post(id={self.id}, title={self.title}), content={self.content}>"

    def increase_view_count(self):
        self.view_count += 1

    def change_likes_count(self, count: int):
        self.likes_count += count
