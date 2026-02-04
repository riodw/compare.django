import decimal
import uuid

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator


class Brand(models.Model):
    name = models.TextField()
    year_founded = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name

    @property
    def uuid(self):
        return self.uuid.id


class Category(models.Model):
    name = models.TextField()
    description = models.TextField()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    @property
    def uuid(self):
        return self.uuid.id


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
        return f"{self.category.name} - {self.name}"

    @property
    def uuid(self):
        return self.uuid.id

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

    @property
    def uuid(self):
        return self.uuid.id


class Source(models.Model):
    name = models.TextField()
    link = models.URLField()
    # FK's
    content_creator = models.ForeignKey(
        ContentCreator,
        related_name="sources",
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = "Source"
        verbose_name_plural = "Sources"

    def __str__(self):
        return self.name

    @property
    def uuid(self):
        return self.uuid.id


class Tool(models.Model):
    name = models.TextField()
    model_number = models.TextField()
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        default=0.00,
    )
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

    @property
    def uuid(self):
        return self.uuid.id


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
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = "Tool Metric"
        verbose_name_plural = "Tool Metrics"

    def __str__(self):
        return f"{self.tool.name} - {self.metric.name}: {self.value}"

    @property
    def uuid(self):
        return self.uuid.id


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
        null=True,
        related_name="uuid",
        on_delete=models.CASCADE,
    )
    category = models.OneToOneField(
        Category,
        null=True,
        related_name="uuid",
        on_delete=models.CASCADE,
    )
    metric = models.OneToOneField(
        Metric,
        null=True,
        related_name="uuid",
        on_delete=models.CASCADE,
    )
    source = models.OneToOneField(
        Source,
        null=True,
        related_name="uuid",
        on_delete=models.CASCADE,
    )
    tool = models.OneToOneField(
        Tool,
        null=True,
        related_name="uuid",
        on_delete=models.CASCADE,
    )
    tool_metric = models.OneToOneField(
        ToolMetric,
        null=True,
        related_name="uuid",
        on_delete=models.CASCADE,
    )
    content_creator = models.OneToOneField(
        ContentCreator,
        null=True,
        related_name="uuid",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "UUID"
        verbose_name_plural = "UUIDs"

    def __str__(self):
        return str(self.id)

    @property
    def uuid(self):
        return self.uuid.id


@receiver(post_save, sender=Brand)
@receiver(post_save, sender=Category)
@receiver(post_save, sender=Metric)
@receiver(post_save, sender=ContentCreator)
@receiver(post_save, sender=Source)
@receiver(post_save, sender=Tool)
@receiver(post_save, sender=ToolMetric)
def create_uuid_model(sender, instance, created, **kwargs):
    if created:
        field_name = sender._meta.model_name
        if sender == ToolMetric:
            field_name = "tool_metric"
        elif sender == ContentCreator:
            field_name = "content_creator"
        UUIDModel.objects.create(**{field_name: instance})
