import bcrypt
from fastapi import HTTPException, status

from member.model.member import Member
from member.repository.member_repository import MemberRepository
from member.schema.member_response import SignUpResponse


class MemberService:
    encoding_type: str = 'utf-8'

    def __init__(self, member_repository: MemberRepository):
        self.repository = member_repository

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
        return SignUpResponse(
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
