from strawberry.fastapi import GraphQLRouter

from app.core.config import settings
from app.presentation.graphql.context import get_graphql_context
from app.presentation.graphql.schema import schema

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_graphql_context,
    graphql_ide="graphiql" if settings.docs_enabled else None,
)
