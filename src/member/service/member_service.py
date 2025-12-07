import bcrypt
from fastapi import HTTPException, status

from auth.repository.refresh_token_repository import RefreshTokenRepository
from auth.utils.jwt_provider import JwtProvider
from member.model.member import Member
from member.repository.member_repository import MemberRepository
from member.schema.member_request import SignUpRequest, UpdateMemberRequest, UpdatePasswordRequest
from member.schema.member_response import MemberResponse


class MemberService:
    encoding_type: str = 'utf-8'

    def __init__(self, member_repository: MemberRepository, token_repository: RefreshTokenRepository):
        self.repository = member_repository
        self.token_repository = token_repository

    def create_member(self, sign_up_request: SignUpRequest) -> MemberResponse:
        if self.repository.find_by_email(str(sign_up_request.email)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미 등록된 이메일입니다.")

        hashed_password: str = self.hash_password(sign_up_request.password)

        member = Member(
            email=str(sign_up_request.email),
            password=hashed_password,
            nickname=sign_up_request.nickname,
            profile_image=sign_up_request.profile_image,
        )

        created = self.repository.save(member)

        return MemberResponse.model_validate(created)

    def hash_password(self, plain_password):
        return bcrypt.hashpw(
            plain_password.encode(self.encoding_type),
            bcrypt.gensalt()
        ).decode(self.encoding_type)

    def verify_password(self, plain_password, hashed_password) -> bool:
        return bcrypt.checkpw(
            plain_password.encode(self.encoding_type),
            hashed_password.encode(self.encoding_type)
        )

    def login(self, email: str, password: str) -> dict:
        member = self.repository.find_by_email(email)
        if not member:
            raise HTTPException(status_code=400, detail="이메일 또는 비밀번호가 틀렸습니다.")

        if not self.verify_password(password, member.password):
            raise HTTPException(status_code=400, detail="이메일 또는 비밀번호가 틀렸습니다.")

        access_token = JwtProvider.create_access_token(member.id)
        refresh_token = JwtProvider.create_refresh_token(member.id)

        self.token_repository.save(token=refresh_token, member_id=member.id)

        return {
            "member": member,
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def logout(self, refresh_token: str):
        self.token_repository.delete_by_token(refresh_token)

    def update_member(self, member_id: int, request: UpdateMemberRequest) -> Member:
        member = self.repository.find_by_id(member_id)
        if not member:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

        if request.nickname is not None:
            member.nickname = request.nickname

        if request.profile_image is not None:
            member.profile_image = request.profile_image

        return self.repository.save(member)

    def delete_member(self, member_id: int):
        member = self.repository.find_by_id(member_id)
        if not member:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
        self.repository.delete(member)

    def update_password(self, member_id: int, request: UpdatePasswordRequest) -> None:
        member = self.repository.find_by_id(member_id)
        if not member:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

        if not self.verify_password(request.old_password, member.password):
            raise HTTPException(status_code=400, detail="기존 비밀번호가 틀렸습니다.")

        new_hashed_password = self.hash_password(request.new_password)
        member.password = new_hashed_password
        self.repository.save(member)
