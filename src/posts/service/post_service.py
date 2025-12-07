from fastapi import HTTPException
from starlette import status

from posts.model.post import Post
from posts.repository.post_repository import PostRepository
from posts.schema.post_request import CreatePostRequest, UpdatePostRequest


class PostService:
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository

    def get_posts(self, skip: int = 0, limit: int = 100, member_id: int | None = None) -> list[Post]:
        posts = self.post_repository.find_all(skip, limit)
        for post in posts:
            post.comments_count = len(post.comments)
            post.likes_count = len(post.likes)
            post.is_liked = any(like.member_id == member_id for like in post.likes) if member_id else False
            post.nickname = post.member.nickname
        return posts

    def get_post(self, post_id: int, member_id: int | None = None) -> Post:
        post = self.post_repository.find_by_id(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

        post.increase_view_count()
        self.post_repository.save(post)

        post.comments_count = len(post.comments)
        post.likes_count = len(post.likes)
        post.is_liked = any(like.member_id == member_id for like in post.likes) if member_id else False
        post.nickname = post.member.nickname

        return post

    def create_post(self, request: CreatePostRequest, member_id: int) -> Post:
        post = Post(
            title=request.title,
            content=request.content,
            article_image=request.article_image_url,
            member_id=member_id
        )
        saved_post = self.post_repository.save(post)

        saved_post.comments_count = 0
        saved_post.likes_count = 0
        saved_post.is_liked = False
        saved_post.nickname = saved_post.member.nickname
        return saved_post

    def update_post(self, post_id: int, request: UpdatePostRequest, member_id: int) -> Post:

        post = self.post_repository.find_by_id(post_id)

        if not post:
            raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

        if post.member_id != member_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="수정 권한이 없습니다.")

        if request.title is not None:
            post.title = request.title
        if request.content is not None:
            post.content = request.content
        if request.article_image_url is not None:
            post.article_image = request.article_image_url

        saved_post = self.post_repository.save(post)

        saved_post.comments_count = len(saved_post.comments)
        saved_post.likes_count = len(saved_post.likes)
        saved_post.is_liked = any(like.member_id == member_id for like in saved_post.likes)
        saved_post.nickname = saved_post.member.nickname
        return saved_post

    def delete_post(self, post_id: int, member_id: int) -> None:

        post = self.post_repository.find_by_id(post_id)

        if not post:
            raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

        if post.member_id != member_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="삭제 권한이 없습니다.")

        self.post_repository.delete(post)
