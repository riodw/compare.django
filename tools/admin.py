from django.contrib import admin
from .models import (
    Brand,
    Category,
    Metric,
    ContentCreator,
    Source,
    Tool,
    ToolMetric,
    WeightedAverage,
    UUIDModel,
)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "link", "year_founded")
    search_fields = ("name",)
    readonly_fields = ("uuid",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    readonly_fields = ("uuid",)


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "unit", "weighting")
    list_filter = ("category",)
    search_fields = ("name", "category__name")
    readonly_fields = ("uuid",)


@admin.register(ContentCreator)
class ContentCreatorAdmin(admin.ModelAdmin):
    list_display = ("name", "link")
    search_fields = ("name",)
    readonly_fields = ("uuid",)


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("category", "content_creator", "link")
    list_filter = ("category", "content_creator")
    search_fields = ("category__name", "content_creator__name")
    readonly_fields = ("uuid",)


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = (
        "brand",
        "name",
        "category",
        "model_number",
        "weight",
        "price",
        "noise_level",
    )
    list_filter = ("brand", "category")
    search_fields = ("name", "brand__name", "model_number")
    readonly_fields = ("uuid",)


@admin.register(ToolMetric)
class ToolMetricAdmin(admin.ModelAdmin):
    list_display = ("tool", "metric", "value", "source")
    list_filter = ("tool__brand", "tool__category", "metric")
    search_fields = ("tool__name", "metric__name")
    readonly_fields = ("uuid",)


@admin.register(WeightedAverage)
class WeightedAverageAdmin(admin.ModelAdmin):
    list_display = ("tool", "source", "score")
    list_filter = ("tool__category",)
    search_fields = ("tool__name",)
    readonly_fields = ("uuid",)


@admin.register(UUIDModel)
class UUIDModelAdmin(admin.ModelAdmin):
    list_display = ("id", "content_object")
    search_fields = ("id",)
    readonly_fields = (
        "id",
        "brand",
        "category",
        "metric",
        "content_creator",
        "source",
        "tool",
        "tool_metric",
        "weighted_average",
    )

    def content_object(self, obj):
        if obj.brand:
            return f"Brand: {obj.brand}"
        if obj.category:
            return f"Category: {obj.category}"
        if obj.metric:
            return f"Metric: {obj.metric}"
        if obj.content_creator:
            return f"ContentCreator: {obj.content_creator}"
        if obj.source:
            return f"Source: {obj.source}"
        if obj.tool:
            return f"Tool: {obj.tool}"
        if obj.tool_metric:
            return f"ToolMetric: {obj.tool_metric}"
        if obj.weighted_average:
            return f"WeightedAverage: {obj.weighted_average}"
        return "-"
