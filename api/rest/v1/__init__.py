from fastapi import APIRouter

from .user import UserRouter

api_router = APIRouter()
api_router.include_router(UserRouter, prefix="/users", tags=["users"])
