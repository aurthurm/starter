from fastapi import Depends
from strawberry.types import Info

from apps.user.service import UserService


# GraphQL Dependency Context
def get_graphql_context(
    user_service: UserService = Depends(),
):
    return {
        "user_service": user_service,
    }


# Extract AuthorService instance from GraphQL context
def get_service(info: Info, service_name: str):
    return info.context[service_name]
