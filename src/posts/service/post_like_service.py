from fastapi import HTTPException

from posts.model.post_like import PostLike
from posts.repository.post_like_repository import PostLikeRepository
from posts.repository.post_repository import PostRepository


class PostLikeService:
    def __init__(
            self,
            post_like_repository: PostLikeRepository,
            post_repository: PostRepository
    ):
        self.post_like_repository = post_like_repository
        self.post_repository = post_repository

    def toggle_like(self, post_id: int, member_id: int) -> dict:

        post = self.post_repository.find_by_id(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="게시글이 존재하지 않습니다.")

        existing_like = self.post_like_repository.find_by_post_and_member(post_id, member_id)

        if existing_like:

            self.post_like_repository.delete(existing_like)
            post.change_likes_count(-1)
            is_liked = False
        else:

            new_like = PostLike(post_id=post_id, member_id=member_id)
            self.post_like_repository.save(new_like)
            post.change_likes_count(1)
            is_liked = True

        self.post_repository.save(post)

        return {"is_liked": is_liked, "likes_count": post.likes_count}
