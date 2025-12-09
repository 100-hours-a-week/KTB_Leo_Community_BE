from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    summary: Optional[str] = None
    article_image: str = None
    member_id: int
    nickname: str
    view_count: int
    likes_count: int
    comments_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
