from fastapi import APIRouter, Depends, status, HTTPException

from repository.member_repository import MemberRepository
from schema.request import SignUpRequest, SignInRequest, MemberInDB
from schema.response import SignUpResponse, JWTRESPONSE
from service.member_service import MemberService

router = APIRouter(prefix="/members")


@router.post("/sign-up", status_code=status.HTTP_201_CREATED, response_model=SignUpResponse)
def sign_up(sign_up_requset: SignUpRequest
            , member_service: MemberService = Depends()):
    try:
        return member_service.create_member(sign_up_requset)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, )


@router.post("/sign-in")
def sign_in(sign_in_requset: SignInRequest,
            member_service: MemberService = Depends(),
            member_repostory: MemberRepository = Depends()):
    member: MemberInDB | None = member_repostory.find_by_email(
        email=sign_in_requset.email
    )
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, )

    verified: bool = member_service.verify_password(
        plain_password=sign_in_requset.password,
        hashed_password=member.hashed_password,
    )
    if not verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )

    access_token: str = member_service.create_jwt(member.email)

    return JWTRESPONSE(access_token=access_token)
