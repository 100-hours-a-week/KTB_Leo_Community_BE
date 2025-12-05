from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from auth.dependencies import get_current_member
from comments.repository.comment_repository import CommentRepository
from comments.schema.comment_request import CreateCommentRequest, UpdateCommentRequest
from comments.schema.comment_response import CommentResponse
from comments.service.comment_service import CommentService
from database.connection import get_db
from member.model.member import Member
from posts.repository.post_repository import PostRepository

router = APIRouter(prefix="/comments", tags=["comments"])


def get_comment_service(db: Session = Depends(get_db)):
    comment_repo = CommentRepository(db)
    post_repo = PostRepository(db)
    return CommentService(comment_repo, post_repo)


@router.get("", response_model=list[CommentResponse])
def get_comments(
        post_id: int,
        service: CommentService = Depends(get_comment_service)
):
    return service.get_comments(post_id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=CommentResponse)
def create_comment(
        request: CreateCommentRequest,
        member: Member = Depends(get_current_member),
        service: CommentService = Depends(get_comment_service)
):
    return service.create_comment(member.id, request)


@router.patch("/{comment_id}", response_model=CommentResponse)
def update_comment(
        comment_id: int,
        request: UpdateCommentRequest,
        member: Member = Depends(get_current_member),
        service: CommentService = Depends(get_comment_service)
):
    return service.update_comment(comment_id, member.id, request)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
        comment_id: int,
        member: Member = Depends(get_current_member),
        service: CommentService = Depends(get_comment_service)
):
    service.delete_comment(comment_id, member.id)
