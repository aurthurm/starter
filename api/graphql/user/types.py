import strawberry


@strawberry.type
class UserType:
    first_name: str
    last_name: str
