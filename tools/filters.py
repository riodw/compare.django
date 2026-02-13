import django_graphene_filters as filters

from . import models


class BrandFilter(filters.AdvancedFilterSet):
    class Meta:
        model = models.Brand
        fields = {
            "name": "__all__",
            "link": "__all__",
            "year_founded": "__all__",
        }


class CategoryFilter(filters.AdvancedFilterSet):
    class Meta:
        model = models.Category
        fields = {
            "name": "__all__",
            "description": "__all__",
        }


class MetricFilter(filters.AdvancedFilterSet):
    class Meta:
        model = models.Metric
        fields = {
            "name": "__all__",
            "description": "__all__",
            "unit": "__all__",
            "weighting": "__all__",
        }


class ContentCreatorFilter(filters.AdvancedFilterSet):
    class Meta:
        model = models.ContentCreator
        fields = {
            "name": "__all__",
            "link": "__all__",
        }


class SourceFilter(filters.AdvancedFilterSet):
    class Meta:
        model = models.Source
        fields = {
            "link": "__all__",
        }


class ToolFilter(filters.AdvancedFilterSet):
    class Meta:
        model = models.Tool
        fields = {
            "name": "__all__",
            "model_number": "__all__",
            "description": "__all__",
            "weight": "__all__",
            "price": "__all__",
            "noise_level": "__all__",
        }


class ToolMetricFilter(filters.AdvancedFilterSet):
    class Meta:
        model = models.ToolMetric
        fields = {
            "value": "__all__",
        }


class WeightedAverageFilter(filters.AdvancedFilterSet):
    class Meta:
        model = models.WeightedAverage
        fields = {
            "score": "__all__",
        }


class UUIDModelFilter(filters.AdvancedFilterSet):
    class Meta:
        model = models.UUIDModel
        fields = {
            "id": "__all__",
        }
