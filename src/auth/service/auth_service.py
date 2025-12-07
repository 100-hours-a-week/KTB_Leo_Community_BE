from fastapi import HTTPException
from sqlalchemy.orm import Session

from auth.repository.refresh_token_repository import RefreshTokenRepository
from auth.utils.jwt_provider import JwtProvider
from member.repository.member_repository import MemberRepository


class AuthService:
    def __init__(self, db: Session):
        self.member_repo = MemberRepository(db)
        self.token_repo = RefreshTokenRepository(db)

    def login(self, email: str, password: str) -> dict:
        member = self.member_repo.find_by_email(email)
        if not member:
            raise HTTPException(status_code=400, detail="아이디 또는 비밀번호 오류")

        access_token = JwtProvider.create_access_token(member.id)
        refresh_token = JwtProvider.create_refresh_token(member.id)

        self.token_repo.save(token=refresh_token, member_id=member.id)

        return {
            "member": member,
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def logout(self, refresh_token: str):
        self.token_repo.delete_by_token(refresh_token)
