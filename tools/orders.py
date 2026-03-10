from graphql import GraphQLError

import django_graphene_filters as orders

from . import models


class BrandOrder(orders.AdvancedOrderSet):
    class Meta:
        model = models.Brand
        fields = [
            "name",
            "link",
            "year_founded",
        ]


class CategoryOrder(orders.AdvancedOrderSet):
    class Meta:
        model = models.Category
        fields = [
            "name",
            "description",
        ]


class MetricOrder(orders.AdvancedOrderSet):
    class Meta:
        model = models.Metric
        fields = [
            "name",
            "description",
            "unit",
            "weighting",
        ]


class ContentCreatorOrder(orders.AdvancedOrderSet):
    class Meta:
        model = models.ContentCreator
        fields = [
            "name",
            "link",
        ]


class SourceOrder(orders.AdvancedOrderSet):
    class Meta:
        model = models.Source
        fields = [
            "link",
        ]


class ToolOrder(orders.AdvancedOrderSet):
    class Meta:
        model = models.Tool
        fields = [
            "name",
            "model_number",
            "description",
            "weight",
            "price",
            "noise_level",
        ]


class ToolMetricOrder(orders.AdvancedOrderSet):
    class Meta:
        model = models.ToolMetric
        fields = [
            "value",
        ]


class WeightedAverageOrder(orders.AdvancedOrderSet):
    class Meta:
        model = models.WeightedAverage
        fields = [
            "score",
        ]


class UUIDModelOrder(orders.AdvancedOrderSet):
    class Meta:
        model = models.UUIDModel
        fields = [
            "id",
        ]
