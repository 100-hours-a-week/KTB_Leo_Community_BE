from typing import Optional

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
        return self.session.query(Member).filter(Member.email == email).first()

    def find_all(self) -> list[type[Member]]:
        return self.session.query(Member).all()
