from sqlalchemy.orm import Session

from posts.model.post import Post


class PostRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_all(self, skip: int = 0, limit: int = 100) -> list[Post]:
        return self.session.query(Post).offset(skip).limit(limit).all()

    def find_by_id(self, post_id: int) -> "Post | None":
        return self.session.query(Post).filter(Post.id == post_id).first()

    def save(self, post: Post) -> Post:
        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)
        return post

    def delete(self, post: Post) -> None:
        self.session.delete(post)
        self.session.commit()
