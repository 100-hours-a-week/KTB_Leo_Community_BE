import bcrypt

from repository.member_repository import MemberRepository
from fastapi import HTTPException, status

from schema.request import MemberInDB
from schema.response import SignUpResponse


class MemberService:
    encoding_type:str = 'utf-8'

    def __init__(self, member_repository: MemberRepository):
        self.repository = member_repository

    def create_member(self, sign_up_requset):
        if self.repository.find_by_email(sign_up_requset.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, )
        hashed_password: str = self.hash_password(sign_up_requset.password)

        member: MemberInDB = MemberInDB(
            id=self.repository.get_next_id(),
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
