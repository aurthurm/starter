from typing import List, Optional

import strawberry
from strawberry.types import Info

from apps.user.protocols import UserServiceProtocol
from core.graphql import get_service

from .types import UserType


@strawberry.type(description="Query all entities")
class UserQuery:
    @strawberry.field(description="Get an Author")
    def user(self, uid: int, info: Info) -> Optional[UserType]:
        user_service: UserServiceProtocol = get_service(info, "user_service")
        return user_service.find(uid)

    @strawberry.field(description="List all Authors")
    def users(self, info: Info) -> List[UserType]:
        user_service: UserServiceProtocol = get_service(info, "user_service")
        return user_service.list()
