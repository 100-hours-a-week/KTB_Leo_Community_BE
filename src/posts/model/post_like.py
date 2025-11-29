from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship

from database.orm import Base


class PostLike(Base):
    __tablename__ = "post_like"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    member_id = Column(Integer, ForeignKey("member.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    __table_args__ = (
        UniqueConstraint('post_id', 'member_id', name='unique_post_like'),
    )

    post = relationship("Post", back_populates="likes")
    member = relationship("Member", back_populates="liked_posts")
