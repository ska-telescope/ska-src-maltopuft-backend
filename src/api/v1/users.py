from fastapi import APIRouter

from src.app.schemas.responses.user import User

user_router = APIRouter()


@user_router.post("/")
async def post_user(user: User):
    return {"name": f"{user.name}"}
