from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from member.model.member import Member


class MemberRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, member: Member) -> Member:
        self.session.add(member)
        self.session.commit()
        self.session.refresh(member)
        return member

    def find_by_email(self, email: str) -> Optional[Member]:
        return self.session.scalar(
            select(Member).where(Member.email == email)
        )

    def find_by_id(self, member_id: int) -> Optional[Member]:
        return self.session.scalar(
            select(Member).where(Member.id == member_id)
        )

    def find_all(self) -> List[Member]:
        return self.session.scalars(select(Member)).all()

    def delete(self, member: Member) -> None:
        self.session.delete(member)
        self.session.commit()
