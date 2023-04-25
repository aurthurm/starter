from fastapi import Depends
from sqlalchemy.orm import Session

from core.database.deps import get_session
from core.database.repository import BaseRepository

from .entities import User


class UserRepository(BaseRepository):
    model = User

    def __init__(self, session_factory: Session = Depends(get_session)):
        self.session_factory = session_factory
