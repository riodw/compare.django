import graphene
from graphene_django import DjangoObjectType

# from graphene_django.types import DjangoObjectType

# from graphene_django.filter import DjangoFilterConnectionField

from django_graphene_filters import AdvancedDjangoFilterConnectionField

from . import models

from . import filters
from . import orders


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
        #     "id": ["exact", "icontains", "istartswith"], }
        orderset_class = orders.BrandOrder


class CategoryNode(DjangoObjectType):
    class Meta:
        model = models.Category
        interfaces = (graphene.Node,)
        connection_class = CountableConnection
        fields = "__all__"
        filterset_class = filters.CategoryFilter
        orderset_class = orders.CategoryOrder


class MetricNode(DjangoObjectType):
    class Meta:
        model = models.Metric
        interfaces = (graphene.Node,)
        connection_class = CountableConnection
        fields = "__all__"
        filterset_class = filters.MetricFilter
        orderset_class = orders.MetricOrder


class ContentCreatorNode(DjangoObjectType):
    class Meta:
        model = models.ContentCreator
        interfaces = (graphene.Node,)
        connection_class = CountableConnection
        fields = "__all__"
        filterset_class = filters.ContentCreatorFilter
        orderset_class = orders.ContentCreatorOrder


class SourceNode(DjangoObjectType):
    class Meta:
        model = models.Source
        interfaces = (graphene.Node,)
        connection_class = CountableConnection
        fields = "__all__"
        filterset_class = filters.SourceFilter
        orderset_class = orders.SourceOrder


class ToolNode(DjangoObjectType):
    class Meta:
        model = models.Tool
        interfaces = (graphene.Node,)
        connection_class = CountableConnection
        fields = "__all__"
        filterset_class = filters.ToolFilter
        orderset_class = orders.ToolOrder


class ToolMetricNode(DjangoObjectType):
    class Meta:
        model = models.ToolMetric
        interfaces = (graphene.Node,)
        connection_class = CountableConnection
        fields = "__all__"
        filterset_class = filters.ToolMetricFilter
        orderset_class = orders.ToolMetricOrder


class WeightedAverageNode(DjangoObjectType):
    class Meta:
        model = models.WeightedAverage
        interfaces = (graphene.Node,)
        connection_class = CountableConnection
        fields = "__all__"
        filterset_class = filters.WeightedAverageFilter
        orderset_class = orders.WeightedAverageOrder


class UUIDModelNode(DjangoObjectType):
    class Meta:
        model = models.UUIDModel
        interfaces = (graphene.Node,)
        connection_class = CountableConnection
        fields = "__all__"
        filterset_class = filters.UUIDModelFilter
        orderset_class = orders.UUIDModelOrder


class Query:
    brand = graphene.Node.Field(BrandNode)
    brands = AdvancedDjangoFilterConnectionField(BrandNode)
    #
    category = graphene.Node.Field(CategoryNode)
    categories = AdvancedDjangoFilterConnectionField(CategoryNode)
    #
    metric = graphene.Node.Field(MetricNode)
    metrics = AdvancedDjangoFilterConnectionField(MetricNode)
    #
    content_creator = graphene.Node.Field(ContentCreatorNode)
    content_creators = AdvancedDjangoFilterConnectionField(ContentCreatorNode)
    #
    source = graphene.Node.Field(SourceNode)
    sources = AdvancedDjangoFilterConnectionField(SourceNode)
    #
    tool = graphene.Node.Field(ToolNode)
    tools = AdvancedDjangoFilterConnectionField(ToolNode)
    #
    tool_metric = graphene.Node.Field(ToolMetricNode)
    tool_metrics = AdvancedDjangoFilterConnectionField(ToolMetricNode)
    #
    weighted_average = graphene.Node.Field(WeightedAverageNode)
    weighted_averages = AdvancedDjangoFilterConnectionField(WeightedAverageNode)
    #
    uuid_model = graphene.Node.Field(UUIDModelNode)
    # all_uuid_models = AdvancedDjangoFilterConnectionField(
    uuid_models = AdvancedDjangoFilterConnectionField(
        UUIDModelNode,
        # filter_input_type_prefix="UUIDModelFilterSetClass",
    )
