import graphene
import tools.schema
from graphene_django.debug import DjangoDebug


class Query(
    tools.schema.Query,
    graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name="_debug")


schema = graphene.Schema(
    query=Query,
)
