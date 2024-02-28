from fastapi import APIRouter

root_router = APIRouter()


@root_router.get("/")
async def read_root():
    return {"data": "Hello world!"}
