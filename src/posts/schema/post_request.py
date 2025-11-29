from pydantic import BaseModel


class CreatePostRequest(BaseModel):
    title: str
    content: str
    article_image_url: str = None
    author_id: int


class UpdatePostRequest(BaseModel):
    title: str = None
    content: str = None
    article_image_url: str = None
