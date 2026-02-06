import decimal
import random
import factory
from factory.django import DjangoModelFactory
from django.core.management.base import BaseCommand
from django.db import transaction
from tools.models import (
    Brand,
    Category,
    Metric,
    ContentCreator,
    Source,
    Tool,
    ToolMetric,
)


class BrandFactory(DjangoModelFactory):
    class Meta:
        model = Brand
        django_get_or_create = ("name",)

    name = factory.Faker("company")
    link = factory.Faker("url")
    year_founded = factory.Faker("year")


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ("name",)

    name = factory.Faker("word")
    description = factory.Faker("sentence")


class MetricFactory(DjangoModelFactory):
    class Meta:
        model = Metric
        django_get_or_create = ("name", "category")

    name = factory.Faker("word")
    description = factory.Faker("sentence")
    unit = factory.Faker("word")
    weighting = factory.Faker("pydecimal", left_digits=0, right_digits=2, positive=True, min_value=0.01, max_value=0.5)
    category = factory.SubFactory(CategoryFactory)


class ContentCreatorFactory(DjangoModelFactory):
    class Meta:
        model = ContentCreator
        django_get_or_create = ("name",)

    name = factory.Faker("name")
    link = factory.Faker("url")


class SourceFactory(DjangoModelFactory):
    class Meta:
        model = Source
        django_get_or_create = ("link",)

    link = factory.Faker("url")
    category = factory.SubFactory(CategoryFactory)
    content_creator = factory.SubFactory(ContentCreatorFactory)


class ToolFactory(DjangoModelFactory):
    class Meta:
        model = Tool

    name = factory.Faker("word")
    model_number = factory.Faker("ean13")
    description = factory.Faker("sentence")
    weight = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    price = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    noise_level = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)


class ToolMetricFactory(DjangoModelFactory):
    class Meta:
        model = ToolMetric

    value = factory.Faker("pydecimal", left_digits=3, right_digits=2)
    tool = factory.SubFactory(ToolFactory)
    metric = factory.SubFactory(MetricFactory)
    source = factory.SubFactory(SourceFactory)


class Command(BaseCommand):
    help = "Populate the database with dummy data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Creating dummy data...")

        # 1. Create Brands
        dewalt = BrandFactory(name="DeWalt")
        makita = BrandFactory(name="Makita")
        ryobi = BrandFactory(name="Ryobi")
        self.stdout.write(f"Created Brands: {dewalt}, {makita}, {ryobi}")

        # 2. Create Categories
        leaf_blower = CategoryFactory(name="Cordless Leaf Blower")
        circular_saw = CategoryFactory(name="Cordless Circular Saw")
        drill = CategoryFactory(name="Cordless Drill")
        self.stdout.write(f"Created Categories: {leaf_blower}, {circular_saw}, {drill}")

        # 3. Create Metrics
        # Cordless Leaf Blower
        MetricFactory(name="Maximum Run Time", category=leaf_blower, unit="Minutes")
        MetricFactory(name="dynamometer (lbs)", category=leaf_blower, unit="lbs")
        MetricFactory(name="Maximum Air Speed", category=leaf_blower, unit="MPH")
        MetricFactory(name="Maximum CFM", category=leaf_blower, unit="CFM")

        # Cordless Circular Saw
        MetricFactory(name="Blade Speed (RPM)", category=circular_saw, unit="RPM")
        MetricFactory(name="Blade Stop Speed", category=circular_saw, unit="Seconds")
        MetricFactory(name="Average Cut Speed - @ 5lbs of pressure", category=circular_saw, unit="Inches/Second")
        MetricFactory(name="Stop-to-Start-to-Stop time", category=circular_saw, unit="Seconds")

        # Cordless Drill
        MetricFactory(name="Highest (No Load) RPM", category=drill, unit="RPM")
        MetricFactory(name="Maximum Working Torque (lbs)", category=drill, unit="lbs")
        MetricFactory(name="Maximum depth hole drilled in concrete", category=drill, unit="Inches")
        MetricFactory(name="Maximum clutch Torque (lbs)", category=drill, unit="lbs")
        MetricFactory(name="Average Driving Speed (5in Lag Bolts)", category=drill, unit="Seconds")
        
        self.stdout.write("Created Metrics")

        # 4. Create ContentCreator
        project_farm = ContentCreatorFactory(
            name="ProjectFarm",
            link="https://www.youtube.com/@ProjectFarm"
        )
        self.stdout.write(f"Created ContentCreator: {project_farm}")

        # 5. Create Sources
        leaf_blower_source = SourceFactory(
            category=leaf_blower,
            content_creator=project_farm,
            link="https://www.youtube.com/watch?v=sqKYiMNvvUg"
        )
        circular_saw_source = SourceFactory(
            category=circular_saw,
            content_creator=project_farm,
            link="https://www.youtube.com/watch?v=7U0bG1exavw"
        )
        drill_source = SourceFactory(
            category=drill,
            content_creator=project_farm,
            link="https://www.youtube.com/watch?v=WVPev_OBq5I"
        )
        self.stdout.write("Created Sources")

        # 6. Create Tools & ToolMetrics
        brands = [dewalt, makita, ryobi]
        category_map = {
            leaf_blower: leaf_blower_source,
            circular_saw: circular_saw_source,
            drill: drill_source,
        }

        for category, source in category_map.items():
            metrics = Metric.objects.filter(category=category)
            for brand in brands:
                 # Create Tool
                tool = ToolFactory(
                    brand=brand,
                    category=category,
                    # Random fields handled by Factory
                )
                
                # Create ToolMetrics for each metric
                for metric in metrics:
                    ToolMetricFactory(
                        tool=tool,
                        metric=metric,
                        source=source,
                        # Value random by Factory
                    )
        
        self.stdout.write(self.style.SUCCESS("Successfully populated dummy data."))
