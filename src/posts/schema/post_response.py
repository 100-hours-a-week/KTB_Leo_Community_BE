from datetime import datetime

from pydantic import BaseModel


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    article_image: str = None
    author_id: int
    view_count: int
    likes_count: int
    comments_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
