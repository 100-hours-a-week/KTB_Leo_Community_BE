from fastapi import FastAPI
from api import member_controller

app = FastAPI()

app.include_router(member_controller.router)


@app.get("/")
async def health_check():
    return {"message": "Hello World"}
