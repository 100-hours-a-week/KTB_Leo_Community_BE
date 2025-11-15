from fastapi import APIRouter, Depends, status, HTTPException

from schema.request import SignUpRequest, SignUpResponse, SignInRequest
from service.member_service import MemberService

router = APIRouter(prefix="/members")

@router.post("/sign-up", status_code=status.HTTP_201_CREATED, response_model=SignUpResponse)
def sign_up(sign_up_requset: SignUpRequest
           , member_service:MemberService = Depends()):
    try:
        return member_service.create_member(sign_up_requset)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,)

