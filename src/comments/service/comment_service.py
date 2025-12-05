from fastapi import HTTPException, status

from comments.model.comment import Comment
from comments.repository.comment_repository import CommentRepository
from comments.schema.comment_request import CreateCommentRequest, UpdateCommentRequest
from posts.repository.post_repository import PostRepository


class CommentService:
    def __init__(self, comment_repository: CommentRepository, post_repository: PostRepository):
        self.comment_repository = comment_repository
        self.post_repository = post_repository

    def get_comments(self, post_id: int) -> list[Comment]:
        return self.comment_repository.find_by_post_id(post_id)

    def create_comment(self, member_id: int, request: CreateCommentRequest) -> Comment:

        found = self.post_repository.find_by_id(request.post_id)
        if not found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시글이 존재하지 않습니다")

        comment = Comment(
            post_id=request.post_id,
            member_id=member_id,
            content=request.content
        )
        return self.comment_repository.save(comment)

    def update_comment(self, comment_id: int, member_id: int, request: UpdateCommentRequest) -> Comment:
        comment = self.comment_repository.find_by_id(comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다.")

        if comment.member_id != member_id:
            raise HTTPException(status_code=403, detail="댓글을 수정할 권한이 없습니다.")

        comment.content = request.content
        return self.comment_repository.save(comment)

    def delete_comment(self, comment_id: int, member_id: int) -> None:
        comment = self.comment_repository.find_by_id(comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다.")

        if comment.member_id != member_id:
            raise HTTPException(status_code=403, detail="댓글을 삭제할 권한이 없습니다.")

        self.comment_repository.delete(comment)
