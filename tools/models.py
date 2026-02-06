import decimal
import uuid

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator


class Brand(models.Model):
    name = models.TextField()
    link = models.URLField()
    year_founded = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.TextField()
    description = models.TextField()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Metric(models.Model):
    name = models.TextField()
    description = models.TextField()
    unit = models.TextField()
    weighting = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[
            MinValueValidator(decimal.Decimal("0.01")),
            MaxValueValidator(decimal.Decimal("1.00")),
        ],
        blank=True,
        default=decimal.Decimal("0.01"),
    )
    # FK's
    category = models.ForeignKey(
        Category,
        related_name="metrics",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ("name", "category")
        verbose_name = "Metric"
        verbose_name_plural = "Metrics"

    def __str__(self):
        return f"{self.category.name} - {self.name} ({self.weighting})"

    def clean(self):
        super().clean()

        # 1. Get all other metrics in the same category
        # We exclude the current instance (self.pk) so we don't double-count
        # when updating an existing record.
        other_metrics = Metric.objects.filter(category=self.category)
        if self.pk:
            other_metrics = other_metrics.exclude(pk=self.pk)

        # 2. Calculate the total weight
        total_weight = sum(m.weighting for m in other_metrics) + self.weighting

        # 3. Validation Logic
        if total_weight > decimal.Decimal("1.00"):
            raise ValidationError(
                {
                    "weighting": "Total weighting cannot exceed 1.00.",
                    "current_total": f"{total_weight}",
                }
            )


class ContentCreator(models.Model):
    name = models.TextField()
    link = models.URLField()

    class Meta:
        verbose_name = "Content Creator"
        verbose_name_plural = "Content Creators"

    def __str__(self):
        return self.name


class Source(models.Model):
    link = models.URLField()
    # FK's
    category = models.ForeignKey(
        Category,
        related_name="sources",
        on_delete=models.CASCADE,
    )
    content_creator = models.ForeignKey(
        ContentCreator,
        related_name="sources",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Source"
        verbose_name_plural = "Sources"

    def __str__(self):
        return f"{self.category.name} ({self.content_creator.name}) - {self.link}"


class Tool(models.Model):
    name = models.TextField()
    model_number = models.TextField()
    description = models.TextField()
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        default=0.00,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        default=0.00,
    )
    # Noise level in dB
    noise_level = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        default=0.00,
    )
    # Should I add tool dimensions?
    # x, y, z
    # FK's
    brand = models.ForeignKey(
        Brand,
        related_name="tools",
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        Category,
        related_name="tools",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Tool"
        verbose_name_plural = "Tools"

    def __str__(self):
        return f"{self.brand.name} {self.name}"


class ToolMetric(models.Model):
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    # FK's
    tool = models.ForeignKey(
        Tool,
        related_name="tool_metrics",
        on_delete=models.CASCADE,
    )
    metric = models.ForeignKey(
        Metric,
        related_name="tool_metrics",
        on_delete=models.CASCADE,
    )
    source = models.ForeignKey(
        Source,
        related_name="tool_metrics",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ("tool", "metric", "source")
        verbose_name = "Tool Metric"
        verbose_name_plural = "Tool Metrics"

    def __str__(self):
        return f"{self.tool.name} - {self.metric.name}: {self.value}"


class WeightedAverage(models.Model):
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )
    # FK's
    tool = models.ForeignKey(
        Tool,
        related_name="weighted_average",
        on_delete=models.CASCADE,
    )
    source = models.ForeignKey(
        Source,
        related_name="weighted_averages",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ("tool", "source")
        verbose_name = "Weighted Average"
        verbose_name_plural = "Weighted Averages"

    def __str__(self):
        return f"{self.tool.name} - Score: {self.score}"


class UUIDModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
    )
    # FK's
    brand = models.OneToOneField(
        Brand,
        related_name="uuid",
        null=True,
        on_delete=models.CASCADE,
    )
    category = models.OneToOneField(
        Category,
        related_name="uuid",
        null=True,
        on_delete=models.CASCADE,
    )
    metric = models.OneToOneField(
        Metric,
        related_name="uuid",
        null=True,
        on_delete=models.CASCADE,
    )
    content_creator = models.OneToOneField(
        ContentCreator,
        related_name="uuid",
        null=True,
        on_delete=models.CASCADE,
    )
    source = models.OneToOneField(
        Source,
        related_name="uuid",
        null=True,
        on_delete=models.CASCADE,
    )
    tool = models.OneToOneField(
        Tool,
        related_name="uuid",
        null=True,
        on_delete=models.CASCADE,
    )
    tool_metric = models.OneToOneField(
        ToolMetric,
        related_name="uuid",
        null=True,
        on_delete=models.CASCADE,
    )
    weighted_average = models.OneToOneField(
        WeightedAverage,
        related_name="uuid",
        null=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "UUID"
        verbose_name_plural = "UUIDs"

    def __str__(self):
        return str(self.id)


@receiver(post_save, sender=Brand)
@receiver(post_save, sender=Category)
@receiver(post_save, sender=Metric)
@receiver(post_save, sender=ContentCreator)
@receiver(post_save, sender=Source)
@receiver(post_save, sender=Tool)
@receiver(post_save, sender=ToolMetric)
@receiver(post_save, sender=WeightedAverage)
def create_uuid_model(sender, instance, created, **kwargs):
    if created:
        field_name = sender._meta.model_name
        if sender == ContentCreator:
            field_name = "content_creator"
        elif sender == ToolMetric:
            field_name = "tool_metric"
        elif sender == WeightedAverage:
            field_name = "weighted_average"
        UUIDModel.objects.create(**{field_name: instance})
