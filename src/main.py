import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from comments.api import comment_controller
from common import file_controller
from member.api import member_controller
from posts.api import post_controller

app = FastAPI()

current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static", "images")

app.mount("/images", StaticFiles(directory=static_dir), name="images")

app.include_router(member_controller.router)
app.include_router(post_controller.router)
app.include_router(comment_controller.router)
app.include_router(file_controller.router)


@app.get("/")
async def health_check():
    return {"message": "Hello World"}
