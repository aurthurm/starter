from typing import List

from fastapi import APIRouter, Depends

from apps.user.models import UserPublic
from apps.user.service import UserService

UserRouter = APIRouter(prefix="/v1/users", tags=["user"])


@UserRouter.get("/", response_model=List[UserPublic])
def index(
    user_service: UserService = Depends(),
):
    return [user.marshall_simple() for user in user_service.all()]
