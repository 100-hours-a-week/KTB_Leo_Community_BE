from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from pydantic.v1 import validator


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    nickname: str
    profile_image: str

    @validator('email')
    def validate_email(self, v):
        if not v or not v.strip():
            raise ValueError('이메일을 입력해주세요')
        return v.strip().lower()


class MemberInDB(BaseModel):
    id: int
    email: str
    password: str
    nickname: str
    profile_image: Optional[str] = None

    class Config:
        from_attributes = True


class SignInRequest(BaseModel):
    email: str
    password: str
