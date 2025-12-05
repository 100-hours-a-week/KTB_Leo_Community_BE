from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from auth.dependencies import get_current_member
from database.connection import get_db
from member.model.member import Member
from posts.repository.post_repository import PostRepository
from posts.schema.post_request import CreatePostRequest, UpdatePostRequest
from posts.schema.post_response import PostResponse
from posts.service.post_service import PostService

router = APIRouter(prefix="/posts")


def get_post_service(db: Session = Depends(get_db)) -> PostService:
    repository = PostRepository(db)
    return PostService(repository)


@router.get("", status_code=status.HTTP_200_OK, response_model=list[PostResponse])
def get_posts(
        skip: int = 0,
        limit: int = 100,
        post_service: PostService = Depends(get_post_service),
):
    return post_service.get_posts(skip, limit)


@router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
def get_post(
        post_id: int,
        service: PostService = Depends(get_post_service),
):
    return service.get_post(post_id)


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
