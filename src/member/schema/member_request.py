from typing import Optional

from pydantic import BaseModel, EmailStr
from pydantic.v1 import validator


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    nickname: str
    profile_image: Optional[str] = None

    @validator('email')
    def validate_email(self, v):
        if not v or not v.strip():
            raise ValueError('이메일을 입력해주세요')
        return v.strip().lower()


class SignInRequest(BaseModel):
    email: str
    password: str


class UpdateMemberRequest(BaseModel):
    nickname: Optional[str] = None
    profile_image: Optional[str] = None


class UpdatePasswordRequest(BaseModel):
    old_password: str
    new_password: str
