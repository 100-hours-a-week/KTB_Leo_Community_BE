from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CommentOwnerResponse(BaseModel):
    id: int
    nickname: str
    profile_image: Optional[str] = None

    class Config:
        from_attributes = True


class CommentResponse(BaseModel):
    id: int
    content: str
    updated_at: datetime

    member: CommentOwnerResponse

    class Config:
        from_attributes = True
