from typing import Optional

from core.database.model import CoreModel, IDModelMixin


class UserBase(CoreModel):
    """
    All common characteristics of our User resource
    """

    first_name: Optional[str]
    last_name: Optional[str]


class UserCreate(UserBase):
    first_name: str
    last_name: str


class UserUpdate(UserBase):
    ...


class UserInDB(IDModelMixin, UserBase):
    first_name: str
    last_name: str


class UserPublic(IDModelMixin, UserBase):
    ...
