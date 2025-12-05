from sqlalchemy.orm import Session

from comments.model.comment import Comment


class CommentRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, comment: Comment) -> Comment:
        self.session.add(comment)
        self.session.commit()
        self.session.refresh(comment)
        return comment

    def find_by_id(self, comment_id: int) -> Comment | None:
        return self.session.query(Comment).filter(Comment.id == comment_id).first()

    def find_by_post_id(self, post_id: int) -> list[Comment]:
        return self.session.query(Comment) \
            .filter(Comment.post_id == post_id) \
            .order_by(Comment.created_at.asc()) \
            .all()

    def delete(self, comment: Comment) -> None:
        self.session.delete(comment)
        self.session.commit()
