from fastapi import HTTPException

from posts.model.post import Post
from posts.repository.post_repository import PostRepository
from posts.schema.post_request import CreatePostRequest, UpdatePostRequest


class PostService:
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository

    def get_posts(self, skip: int = 0, limit: int = 100) -> list[Post]:
        return self.post_repository.find_all(skip, limit)

    def get_post(self, post_id: int) -> Post:
        post = self.post_repository.find_by_id(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post

    def create_post(self, request: CreatePostRequest) -> Post:
        post = Post(
            title=request.title,
            content=request.content,
            article_image=request.article_image_url,
            author_id=request.author_id
        )
        return self.post_repository.save(post)

    def update_post(self, post_id: int, request: UpdatePostRequest) -> Post:
        post = self.get_post(post_id)

        if request.title is not None:
            post.title = request.title
        if request.content is not None:
            post.content = request.content
        if request.article_image_url is not None:
            post.article_image = request.article_image_url

        return self.post_repository.save(post)

    def delete_post(self, post_id: int) -> None:
        post = self.get_post(post_id)
        self.post_repository.delete(post)
