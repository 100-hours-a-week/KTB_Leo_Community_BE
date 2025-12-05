from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from common import file_controller
from member.api import member_controller
from posts.api import post_controller

app = FastAPI()

app.mount("/images", StaticFiles(directory="static/images"), name="images")

app.include_router(member_controller.router)
app.include_router(post_controller.router)
app.include_router(file_controller.router)


@app.get("/")
async def health_check():
    return {"message": "Hello World"}
