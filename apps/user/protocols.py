from typing import Protocol, TypeVar

from .entities import User

UserType = TypeVar("UserType", bound=User)


class UserServiceProtocol(Protocol):
    def create(self, user) -> UserType:
        ...

    def find(self, uid: str) -> UserType:
        ...
