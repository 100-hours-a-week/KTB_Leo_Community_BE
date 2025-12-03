import bcrypt
from fastapi import HTTPException, status

from auth.repository.refresh_token_repository import RefreshTokenRepository
from auth.utils.jwt_provider import JwtProvider
from member.model.member import Member
from member.repository.member_repository import MemberRepository
from member.schema.member_response import MemberResponse


class MemberService:
    encoding_type: str = 'utf-8'

    def __init__(self, member_repository: MemberRepository, token_repository: RefreshTokenRepository):
        self.repository = member_repository
        self.token_repository = token_repository

    def create_member(self, sign_up_requset):
        if self.repository.find_by_email(sign_up_requset.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        hashed_password: str = self.hash_password(sign_up_requset.password)

        member = Member(
            email=sign_up_requset.email,
            password=hashed_password,
            nickname=sign_up_requset.nickname,
            profile_image=sign_up_requset.profile_image,
        )

        created = self.repository.save(member)
        return MemberResponse(
            id=created.id,
            email=created.email,
            nickname=created.nickname,
            profile_image=created.profile_image
        )

    def hash_password(self, plain_password):
        hashed_password = bcrypt.hashpw(plain_password.encode(self.encoding_type),
                                        salt=bcrypt.gensalt()
                                        )
        return hashed_password.decode(self.encoding_type)

    def verify_password(self, plain_password, hashed_password) -> bool:
        # todo : 예외처리
        return bcrypt.checkpw(plain_password.encode(self.encoding_type),
                              hashed_password.encode(self.encoding_type))

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
