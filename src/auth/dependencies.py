from fastapi import Request, HTTPException, Depends, status
from sqlalchemy.orm import Session

from auth.utils import JwtUtils
from database.connection import get_db
from member.model.member import Member
from member.repository.member_repository import MemberRepository


def get_current_member(
        request: Request,
        db: Session = Depends(get_db)
) -> Member:
    access_token = request.cookies.get("accessToken")

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증 토큰이 쿠키에 없습니다."
        )

    member_id = JwtUtils.decode_token(access_token)
    if not member_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않거나 만료된 토큰입니다."
        )

    member_repository = MemberRepository(db)
    member = member_repository.session.query(Member).filter(Member.id == int(member_id)).first()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="존재하지 않는 사용자입니다."
        )

    return member


def get_refresh_token_from_cookie(request: Request) -> str:
    refresh_token = request.cookies.get("refreshToken")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="리프레시 토큰이 없습니다."
        )
    return refresh_token
