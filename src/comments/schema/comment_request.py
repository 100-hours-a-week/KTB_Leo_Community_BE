from pydantic import BaseModel


class CreateCommentRequest(BaseModel):
    post_id: int
    content: str


class UpdateCommentRequest(BaseModel):
    content: str
