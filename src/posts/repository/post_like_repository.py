from sqlalchemy.orm import Session
from posts.model.post_like import PostLike

class PostLikeRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, post_like: PostLike) -> PostLike:
        self.session.add(post_like)
        self.session.commit()
        return post_like

    def delete(self, post_like: PostLike) -> None:
        self.session.delete(post_like)
        self.session.commit()

    def find_by_post_and_member(self, post_id: int, member_id: int) -> PostLike | None:
        return self.session.query(PostLike).filter(
            PostLike.post_id == post_id,
            PostLike.member_id == member_id
        ).first()