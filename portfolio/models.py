from django.db import models
from django.urls import reverse


class Destination(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    tagline = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to="destinations/")

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse(
            "portfolio:destination_detail",
            kwargs={"slug": self.slug},
        )

    def __str__(self):
        return self.name


class Service(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True)

    def get_absolute_url(self):
        return reverse(
            "services:detail",
            kwargs={"slug": self.slug},
        )

    def __str__(self):
        return self.title


class ServiceFeature(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="features",
    )

    text = models.CharField(max_length=150)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.text


class Property(models.Model):

    PROPERTY_TYPES = [
        ("villa", "Villa"),
        ("farmhouse", "Farmhouse"),
        ("estate", "Estate"),
        ("country_home", "Country Home"),
    ]

    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)

    destination = models.ForeignKey(
        Destination,
        on_delete=models.PROTECT,
        related_name="properties",
    )

    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPES,
    )

    description = models.TextField()

    bedrooms = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    bathrooms = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
    )

    sleeps = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    land_size_hectares = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    services = models.ManyToManyField(
        Service,
        related_name="properties",
        blank=True,
    )

    cover_image = models.ImageField(
        upload_to="properties/covers/",
    )

    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Properties"
        ordering = ["-featured", "title"]

    def get_absolute_url(self):
        return reverse(
            "portfolio:property_detail",
            kwargs={"slug": self.slug},
        )

    def __str__(self):
        return self.title


class PropertyImage(models.Model):

    class Section(models.TextChoices):
        ARRIVAL = "arrival", "Arrival"
        EXTERIOR = "exterior", "Exterior"
        LIVING = "living", "Living Spaces"
        BEDROOMS = "bedrooms", "Bedrooms"
        OUTDOORS = "outdoors", "Outdoor Living"
        GARDENS = "gardens", "Gardens & Grounds"
        DETAILS = "details", "Architectural Details"
        VIEWS = "views", "Views"

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="gallery",
    )

    image = models.ImageField(
        upload_to="properties/gallery/",
    )

    section = models.CharField(
        max_length=20,
        choices=Section.choices,
        default=Section.EXTERIOR,
    )

    caption = models.CharField(
        max_length=255,
        blank=True,
    )

    order = models.PositiveSmallIntegerField(
        default=0,
    )

    class Meta:
        ordering = [
            "section",
            "order",
            "pk",
        ]

    def __str__(self):
        return (
            f"{self.property.title} — "
            f"{self.get_section_display()}"
        )


class Testimonial(models.Model):
    quote = models.TextField()

    author_name = models.CharField(max_length=100)

    destination = models.ForeignKey(
        Destination,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="testimonials",
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="testimonials",
    )

    featured_on_homepage = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.author_name}: {self.quote[:40]}..."