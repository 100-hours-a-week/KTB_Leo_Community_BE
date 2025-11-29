from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from database.orm import Base


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True, autoincrement=True)

    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    member_id = Column(Integer, ForeignKey('member.id'), nullable=False)
    content = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    post = relationship("Post", back_populates="comments")
    member = relationship("Member", back_populates="comments")
