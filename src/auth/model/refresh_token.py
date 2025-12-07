from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from database.orm import Base


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    token = Column(String(255), unique=True, index=True, nullable=False)
    member_id = Column(Integer, ForeignKey("member.id"), nullable=False)

    member = relationship("Member", back_populates="refresh_tokens")

    deleted = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<RefreshToken(id={self.id}, member_id={self.member_id}, deleted={self.deleted})>"
