from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from auth.utils import JwtUtils
from database.connection import get_db
from member.model.member import Member
from member.repository.member_repository import MemberRepository
from member.schema.member_request import SignUpRequest, SignInRequest
from member.schema.member_response import SignUpResponse
from member.service.member_service import MemberService

router = APIRouter(prefix="/members")


def get_member_repository(session: Session = Depends(get_db)):
    return MemberRepository(session)


def get_member_service(member_repository: MemberRepository = Depends(get_member_repository)):
    return MemberService(member_repository)


@router.post("/sign-up", status_code=status.HTTP_201_CREATED, response_model=SignUpResponse)
def sign_up(sign_up_requset: SignUpRequest,
            member_service: MemberService = Depends(get_member_service)):
    try:
        return member_service.create_member(sign_up_requset)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/sign-in")
def sign_in(response: Response,
            sign_in_requset: SignInRequest,
            member_service: MemberService = Depends(get_member_service),
            member_repository: MemberRepository = Depends(get_member_repository)):
    member: Member | None = member_repository.find_by_email(
        email=sign_in_requset.email
    )
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="가입되지 않은 회원입니다")

    verified: bool = member_service.verify_password(
        plain_password=sign_in_requset.password,
        hashed_password=member.password,
    )
    if not verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="이메일 또는 비밀번호가 틀렸습니다.")

    access_token = JwtUtils.create_access_token(member.id)
    refresh_token = JwtUtils.create_refresh_token(member.id)

    response.set_cookie(
        key="accessToken",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="Lax"
    )
    response.set_cookie(
        key="refreshToken",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="Lax"
    )

    return {"message": "Login Successful"}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("accessToken")
    response.delete_cookie("refreshToken")
    return {"message": "Logout Successful"}
