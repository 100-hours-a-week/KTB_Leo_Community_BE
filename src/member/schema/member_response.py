from typing import Optional

from pydantic import BaseModel


class MemberResponse(BaseModel):
    id: int
    email: str
    nickname: str
    profile_image: Optional[str] = None

    class Config:
        from_attributes = True
