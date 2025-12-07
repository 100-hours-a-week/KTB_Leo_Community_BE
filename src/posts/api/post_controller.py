from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from auth.dependencies import get_current_member, get_optional_current_member
from database.connection import get_db
from member.model.member import Member
from posts.repository.post_like_repository import PostLikeRepository
from posts.repository.post_repository import PostRepository
from posts.schema.post_request import CreatePostRequest, UpdatePostRequest
from posts.schema.post_response import PostResponse
from posts.service.post_like_service import PostLikeService
from posts.service.post_service import PostService

router = APIRouter(prefix="/posts")


def get_post_service(db: Session = Depends(get_db)) -> PostService:
    repository = PostRepository(db)
    return PostService(repository)


def get_post_like_service(db: Session = Depends(get_db)):
    like_repository = PostLikeRepository(db)
    post_repository = PostRepository(db)
    return PostLikeService(like_repository, post_repository)


@router.get("", status_code=status.HTTP_200_OK, response_model=list[PostResponse])
def get_posts(
        skip: int = 0,
        limit: int = 100,
        member: Member | None = Depends(get_optional_current_member),
        post_service: PostService = Depends(get_post_service),
):
    member_id = member.id if member else None
    return post_service.get_posts(skip, limit, member_id)


@router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
def get_post(
        post_id: int,
        member: Member | None = Depends(get_optional_current_member),
        service: PostService = Depends(get_post_service),
):
    member_id = member.id if member else None
    return service.get_post(post_id, member_id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(
        request: CreatePostRequest,
        member: Member = Depends(get_current_member),
        service: PostService = Depends(get_post_service)
):
    return service.create_post(request, member.id)


@router.patch("/{post_id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
def update_post(
        post_id: int,
        request: UpdatePostRequest,
        member: Member = Depends(get_current_member),
        service: PostService = Depends(get_post_service)
):
    return service.update_post(post_id, request, member.id)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
        post_id: int,
        member: Member = Depends(get_current_member),
        service: PostService = Depends(get_post_service)
):
    service.delete_post(post_id, member.id)


@router.post("/{post_id}/like", status_code=status.HTTP_200_OK)
def like_post(
        post_id: int,
        member: Member = Depends(get_current_member),
        like_service: PostLikeService = Depends(get_post_like_service),
):
    return like_service.toggle_like(post_id, member.id)
