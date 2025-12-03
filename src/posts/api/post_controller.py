from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from database.connection import get_db
from member.model.member import Member
from member.repository.member_repository import MemberRepository
from member.service.member_service import MemberService
from posts.repository.post_repository import PostRepository
from posts.schema.post_request import CreatePostRequest, UpdatePostRequest
from posts.schema.post_response import PostResponse
from posts.service.post_service import PostService
from security import get_access_token

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
        access_token=Depends(get_access_token),
        service: PostService = Depends(get_post_service),
        member_service: MemberService = Depends(),
        member_repository: MemberRepository = Depends(),
):
    member_email = member_service.decode_jwt(access_token)
    member: Member | None = member_repository.find_by_email(member_email)
    if not member:
        raise HTTPException(status_code=404, detail="Not found")

    return service.get_post(post_id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(
        request: CreatePostRequest,
        service: PostService = Depends(get_post_service)
):
    return service.create_post(request)


@router.patch("/{post_id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
def update_post(
        post_id: int,
        request: UpdatePostRequest,
        service: PostService = Depends(get_post_service)
):
    return service.update_post(post_id, request)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
        post_id: int,
        service: PostService = Depends(get_post_service)
):
    service.delete_post(post_id)
