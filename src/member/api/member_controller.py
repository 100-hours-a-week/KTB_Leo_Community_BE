from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from database.connection import get_db
from member.model.member import Member
from member.repository.member_repository import MemberRepository
from member.schema.member_request import SignUpRequest, SignInRequest
from member.schema.member_response import SignUpResponse, JWTRESPONSE
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
def sign_in(sign_in_requset: SignInRequest,
            member_service: MemberService = Depends(get_member_service),
            member_repository: MemberRepository = Depends(get_member_repository)):
    member: Member | None = member_repository.find_by_email(
        email=sign_in_requset.email
    )
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")

    verified: bool = member_service.verify_password(
        plain_password=sign_in_requset.password,
        hashed_password=member.password,
    )
    if not verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

    access_token: str = member_service.create_jwt(member.email)

    return JWTRESPONSE(access_token=access_token)
