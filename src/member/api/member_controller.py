
from fastapi import APIRouter, Depends, status, Response, Request
from sqlalchemy.orm import Session

from auth.dependencies import get_current_member
from auth.repository.refresh_token_repository import RefreshTokenRepository
from auth.utils.cookie_manager import CookieManager
from database.connection import get_db
from member.model.member import Member
from member.repository.member_repository import MemberRepository
from member.schema.member_request import SignUpRequest, SignInRequest, UpdateMemberRequest, UpdatePasswordRequest
from member.schema.member_response import MemberResponse
from member.service.member_service import MemberService

router = APIRouter(prefix="/members", tags=["members"])


def get_member_service(db: Session = Depends(get_db)):
    member_repo = MemberRepository(db)
    token_repo = RefreshTokenRepository(db)
    return MemberService(member_repo, token_repo)


@router.post("/sign-up", status_code=status.HTTP_201_CREATED, response_model=MemberResponse)
def sign_up(
        request: SignUpRequest,
        member_service: MemberService = Depends(get_member_service)
):
    return member_service.create_member(request)


@router.post("/sign-in", response_model=MemberResponse)
def sign_in(
        response: Response,
        request: SignInRequest,
        service: MemberService = Depends(get_member_service)
):
    login_result = service.login(request.email, request.password)

    CookieManager.set_login_cookies(
        response=response,
        access_token=login_result["access_token"],
        refresh_token=login_result["refresh_token"]
    )

    return MemberResponse.model_validate(login_result["member"])


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


@router.get("/me", response_model=MemberResponse)
def get_my_profile(
        member: Member = Depends(get_current_member)
):
    return MemberResponse.model_validate(member)


@router.patch("/me", response_model=MemberResponse)
def update_my_profile(
        request: UpdateMemberRequest,
        member: Member = Depends(get_current_member),
        service: MemberService = Depends(get_member_service)
):
    return service.update_member(member.id, request)


@router.patch("/password", status_code=status.HTTP_200_OK)
def update_password(
        request: UpdatePasswordRequest,
        member: Member = Depends(get_current_member),
        service: MemberService = Depends(get_member_service)
):
    service.update_password(member.id, request)
    return {"message": "비밀번호가 성공적으로 변경되었습니다."}


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def withdraw_member(
        response: Response,
        member: Member = Depends(get_current_member),
        service: MemberService = Depends(get_member_service)
):
    service.delete_member(member.id)
    CookieManager.clear_login_cookies(response)
