import strawberry  # noqa

from .user.query import UserQuery


@strawberry.type
class Query(
    UserQuery,
):
    pass


# @strawberry.type
# class Mutation(
# ):
#     pass


# @strawberry.type
# class Subscription():
#     pass


gql_schema = strawberry.Schema(
    query=Query  # , mutation=Mutation, subscription=Subscription
)
