from sqlalchemy.orm import Session

from auth.model.refresh_token import RefreshToken


class RefreshTokenRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, token: str, member_id: int) -> RefreshToken:
        refresh_token = RefreshToken(token=token, member_id=member_id)
        self.session.add(refresh_token)
        self.session.commit()
        return refresh_token

    def delete_by_token(self, token: str):
        self.session.query(RefreshToken). \
            filter(RefreshToken.token == token). \
            update({"deleted": True})
        self.session.commit()

    def find_valid_token(self, token: str) -> RefreshToken | None:
        return self.session.query(RefreshToken). \
            filter(RefreshToken.token == token). \
            filter(RefreshToken.deleted == False). \
            first()
