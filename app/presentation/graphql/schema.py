import strawberry

from app.presentation.graphql.resolvers.mutation import Mutation
from app.presentation.graphql.resolvers.query import Query

schema = strawberry.Schema(query=Query, mutation=Mutation)
