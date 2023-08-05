from fastapi import Depends

from core.database.protocols import RepositoryProtocol

from .entities import User
from .repository import UserRepository


class UserService:
    repository: RepositoryProtocol

    def __init__(self, repository: UserRepository = Depends()):
        self.repository = repository

    def create(self, user) -> User:
        return self.repository.create({})
