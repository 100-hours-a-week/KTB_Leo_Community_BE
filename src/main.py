from fastapi import FastAPI

from member.api import member_controller
from posts.api import post_controller

app = FastAPI()

app.include_router(member_controller.router)
app.include_router(post_controller.router)


@app.get("/")
async def health_check():
    return {"message": "Hello World"}
