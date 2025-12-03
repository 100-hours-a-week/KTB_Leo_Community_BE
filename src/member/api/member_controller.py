from fastapi import APIRouter, Depends, status, HTTPException, Response, Request
from sqlalchemy.orm import Session

from auth.repository.refresh_token_repository import RefreshTokenRepository
from auth.utils.cookie_manager import CookieManager
from database.connection import get_db
from member.repository.member_repository import MemberRepository
from member.schema.member_request import SignUpRequest, SignInRequest
from member.schema.member_response import MemberResponse
from member.service.member_service import MemberService

router = APIRouter(prefix="/members")


def get_member_repository(session: Session = Depends(get_db)):
    return MemberRepository(session)


def get_member_service(db: Session = Depends(get_db)):
    member_repo = MemberRepository(db)
    token_repo = RefreshTokenRepository(db)
    return MemberService(member_repo, token_repo)


@router.post("/sign-up", status_code=status.HTTP_201_CREATED, response_model=MemberResponse)
def sign_up(sign_up_requset: SignUpRequest,
            member_service: MemberService = Depends(get_member_service)):
    try:
        return member_service.create_member(sign_up_requset)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/sign-in", response_model=MemberResponse)
def sign_in(
        response: Response,
        sign_in_request: SignInRequest,
        service: MemberService = Depends(get_member_service)
):
    login_result = service.login(sign_in_request.email, sign_in_request.password)

    CookieManager.set_login_cookies(
        response=response,
        access_token=login_result["access_token"],
        refresh_token=login_result["refresh_token"]
    )

    return MemberResponse.from_orm(login_result["member"])


@router.post("/logout")
def logout(
        request: Request,
        response: Response,
        service: MemberService = Depends(get_member_service)
):
    refresh_token = request.cookies.get("refreshToken")

    if refresh_token:
        service.logout(refresh_token)

    CookieManager.clear_login_cookies(response)

    return {"message": "Logout Successful"}
