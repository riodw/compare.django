import graphene
from graphene_django import DjangoObjectType, DjangoListField

# from graphene_django.filter import DjangoFilterConnectionField
from django_graphene_filters import AdvancedDjangoFilterConnectionField

from . import models
from . import filters


class CountableConnection(graphene.relay.Connection):
    class Meta:
        abstract = True

    count = graphene.Int(
        description="Total of objects in this connection.",
        required=True,
    )
    counts = graphene.Int(
        description="Count of objects in this edge.",
        required=True,
    )

    def resolve_count(root, info, **kwargs):
        return root.length

    def resolve_counts(root, info, **kwargs):
        return len(root.edges)


class UUID(DjangoObjectType):
    class Meta:
        model = models.UUID
        fields = "__all__"
        # fields = ["address"]
        filter_fields = {
            "address": ["exact"],
        }
        interfaces = (graphene.relay.Node,)
        connection_class = CountableConnection


class Address(DjangoObjectType):
    class Meta:
        model = models.Address
        fields = "__all__"
        filterset_class = filters.AddressFilter
        interfaces = (graphene.relay.Node,)
        connection_class = CountableConnection


class House(DjangoObjectType):
    class Meta:
        model = models.House
        fields = "__all__"
        filterset_class = filters.HouseFilter
        # filter_fields = {"name": ["exact", "icontains", "istartswith"],}
        interfaces = (graphene.relay.Node,)
        connection_class = CountableConnection


class Query(graphene.ObjectType):
    # address = AdvancedDjangoFilterConnectionField(
    #     Address,
    #     filter_input_type_prefix="AddressFilterSetClass",
    #     description="Advanced filter fields for Address model",
    # )
    houses = AdvancedDjangoFilterConnectionField(
        House,
        filter_input_type_prefix="HouseFilterSetClass",
        description="Advanced filter fields for House model",
    )
    # uuid = AdvancedDjangoFilterConnectionField(
    #     UUID,
    #     filter_input_type_prefix="UUIDFilterSetClass",
    #     description="Advanced filter fields for UUID model",
    # )
    # houses = AdvancedDjangoFilterConnectionField(House)
    # house = graphene.Field(House, id=graphene.Int())

    # def resolve_house(root, info, id):
    #     try:
    #         return models.House.objects.get(id=id)
    #     except models.House.DoesNotExist:
    #         return None

    # def resolve_houses(root, info):
    #     if info.context.user.is_authenticated:
    #         return models.House.objects.all()
    #     else:
    #         return models.House.objects.none()


# class Mutation(graphene.ObjectType):
#     pass


schema = graphene.Schema(
    query=Query,
    #  mutation=Mutation,
)