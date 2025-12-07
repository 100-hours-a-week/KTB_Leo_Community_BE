from typing import Optional

from pydantic import BaseModel, ConfigDict


class MemberResponse(BaseModel):
    id: int
    email: str
    nickname: str
    profile_image: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
