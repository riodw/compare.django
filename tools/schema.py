import graphene
from graphene_django import DjangoObjectType

# from graphene_django.types import DjangoObjectType

from graphene_django.filter import DjangoFilterConnectionField

# from django_graphene_filters import AdvancedDjangoFilterConnectionField

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


"""
Nodes
"""


class BrandNode(DjangoObjectType):
    class Meta:
        model = models.Brand
        interfaces = (graphene.Node,)
        connection_class = CountableConnection
        fields = "__all__"
        filterset_class = filters.BrandFilter
        # filter_fields = {
        #     "id": ["exact", "icontains", "istartswith"],
        # }


class CategoryNode(DjangoObjectType):
    class Meta:
        model = models.Category
        interfaces = (graphene.Node,)
        connection_class = CountableConnection
        fields = "__all__"
        filterset_class = filters.CategoryFilter
        # filter_fields = {
        #     "id": ["exact", "icontains", "istartswith"],
        # }


class MetricNode(DjangoObjectType):
    class Meta:
        model = models.Metric
        interfaces = (graphene.Node,)
        connection_class = CountableConnection
        fields = "__all__"
        filterset_class = filters.MetricFilter
        # filter_fields = {
        #     "id": ["exact", "icontains", "istartswith"],
        # }


class ContentCreatorNode(DjangoObjectType):
    class Meta:
        model = models.ContentCreator
        interfaces = (graphene.Node,)
        connection_class = CountableConnection
        fields = "__all__"
        filterset_class = filters.ContentCreatorFilter
        # filter_fields = {
        #     "id": ["exact", "icontains", "istartswith"],
        # }


class SourceNode(DjangoObjectType):
    class Meta:
        model = models.Source
        interfaces = (graphene.Node,)
        connection_class = CountableConnection
        fields = "__all__"
        filterset_class = filters.SourceFilter
        # filter_fields = {
        #     "id": ["exact", "icontains", "istartswith"],
        # }


class ToolNode(DjangoObjectType):
    class Meta:
        model = models.Tool
        interfaces = (graphene.Node,)
        connection_class = CountableConnection
        fields = "__all__"
        filterset_class = filters.ToolFilter
        # filter_fields = {
        #     "id": ["exact", "icontains", "istartswith"],
        # }


class ToolMetricNode(DjangoObjectType):
    class Meta:
        model = models.ToolMetric
        interfaces = (graphene.Node,)
        connection_class = CountableConnection
        fields = "__all__"
        filterset_class = filters.ToolMetricFilter
        # filter_fields = {
        #     "id": ["exact", "icontains", "istartswith"],
        # }


class WeightedAverageNode(DjangoObjectType):
    class Meta:
        model = models.WeightedAverage
        interfaces = (graphene.Node,)
        connection_class = CountableConnection
        fields = "__all__"
        filterset_class = filters.WeightedAverageFilter
        # filter_fields = {
        #     "id": ["exact", "icontains", "istartswith"],
        # }


class UUIDModelNode(DjangoObjectType):
    class Meta:
        model = models.UUIDModel
        interfaces = (graphene.Node,)
        connection_class = CountableConnection
        fields = "__all__"
        filterset_class = filters.UUIDModelFilter
        # filter_fields = {
        #     "id": ["exact", "icontains", "istartswith"],
        # }


class Query:
    brand = graphene.Node.Field(BrandNode)
    all_brands = DjangoFilterConnectionField(BrandNode)
    #
    category = graphene.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)
    #
    metric = graphene.Node.Field(MetricNode)
    all_metrics = DjangoFilterConnectionField(MetricNode)
    #
    content_creator = graphene.Node.Field(ContentCreatorNode)
    all_content_creators = DjangoFilterConnectionField(ContentCreatorNode)
    #
    source = graphene.Node.Field(SourceNode)
    all_sources = DjangoFilterConnectionField(SourceNode)
    #
    tool = graphene.Node.Field(ToolNode)
    all_tools = DjangoFilterConnectionField(ToolNode)
    #
    tool_metric = graphene.Node.Field(ToolMetricNode)
    all_tool_metrics = DjangoFilterConnectionField(ToolMetricNode)
    #
    weighted_average = graphene.Node.Field(WeightedAverageNode)
    all_weighted_averages = DjangoFilterConnectionField(WeightedAverageNode)
    #
    uuid_model = graphene.Node.Field(UUIDModelNode)
    # all_uuid_models = AdvancedDjangoFilterConnectionField(
    all_uuid_models = DjangoFilterConnectionField(
        UUIDModelNode,
        # filter_input_type_prefix="UUIDModelFilterSetClass",
    )
