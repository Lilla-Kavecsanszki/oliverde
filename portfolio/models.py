import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class Destination(models.Model):
    """A geographic area represented in the public portfolio."""

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
    """A property-management service offered by Oliverde."""

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
    """An ordered feature displayed on a service page."""

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="features",
    )
    text = models.CharField(max_length=150)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "pk"]

    def __str__(self):
        return self.text


class ServiceImage(models.Model):
    """An ordered image in a service-page gallery."""

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="gallery",
    )

    image = models.ImageField(
        upload_to="services/gallery/",
    )

    caption = models.CharField(
        max_length=255,
        blank=True,
    )

    alt_text = models.CharField(
        max_length=255,
        blank=True,
        help_text=(
            "A short description of the image for accessibility and "
            "search engines."
        ),
    )

    order = models.PositiveSmallIntegerField(
        default=0,
    )

    class Meta:
        ordering = (
            "order",
            "pk",
        )
        verbose_name = "service image"
        verbose_name_plural = "service images"

    def __str__(self):
        return f"{self.service.title} — image {self.order or self.pk}"


class PropertyAmenity(models.Model):
    """A reusable property highlight selected in Django Admin."""

    class Category(models.TextChoices):
        COMFORT = "comfort", "Comfort"
        OUTDOOR = "outdoor", "Outdoor Living"
        PRACTICAL = "practical", "Practical"
        SERVICES = "services", "Optional Services"

    name = models.CharField(max_length=80, unique=True)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
    )
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Property amenities"
        ordering = ["category", "order", "name"]

    def __str__(self):
        return self.name


class Property(models.Model):
    """A property managed by Oliverde and optionally offered for rental."""

    class PropertyType(models.TextChoices):
        VILLA = "villa", "Villa"
        FARMHOUSE = "farmhouse", "Farmhouse"
        ESTATE = "estate", "Estate"
        COUNTRY_HOME = "country_home", "Country Home"

    class AirConditioning(models.TextChoices):
        NONE = "none", "No Air Conditioning"
        PARTIAL = "partial", "Air Conditioning in Selected Rooms"
        BEDROOMS = "bedrooms", "Air Conditioning in Bedrooms"
        THROUGHOUT = "throughout", "Air Conditioning Throughout"

    class PoolType(models.TextChoices):
        NONE = "none", "No Swimming Pool"
        PRIVATE = "private", "Private Swimming Pool"
        SHARED = "shared", "Shared Swimming Pool"

    # Internal identity and public privacy controls.
    title = models.CharField(
        max_length=150,
        help_text=(
            "Internal property name used by the Oliverde team. It remains "
            "private unless public use is approved."
        ),
    )
    public_title = models.CharField(
        max_length=150,
        blank=True,
        help_text=(
            "Privacy-safe public name, for example 'The Cypress Estate' or "
            "'Olive Grove House'."
        ),
    )
    show_real_name_publicly = models.BooleanField(
        default=False,
        help_text=(
            "Enable only when the owner has approved public use of the "
            "property's real name."
        ),
    )
    public_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        help_text=(
            "Random public identifier used in the property URL. This prevents "
            "the internal property name from appearing in or being inferred "
            "from the URL."
        ),
    )
    slug = models.SlugField(
        unique=True,
        help_text=(
            "Privacy-safe editorial slug. Never use the property's real "
            "internal name unless publication has been approved."
        ),
    )

    # Core property information.
    destination = models.ForeignKey(
        Destination,
        on_delete=models.PROTECT,
        related_name="properties",
    )
    property_type = models.CharField(
        max_length=20,
        choices=PropertyType.choices,
    )
    description = models.TextField()
    bedrooms = models.PositiveSmallIntegerField(null=True, blank=True)
    bathrooms = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
    )
    sleeps = models.PositiveSmallIntegerField(null=True, blank=True)
    land_size_hectares = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    # Comfort and pool information.
    air_conditioning = models.CharField(
        max_length=20,
        choices=AirConditioning.choices,
        default=AirConditioning.NONE,
        help_text=(
            "Select the general air-conditioning arrangement. Use the details "
            "field for room-specific information."
        ),
    )
    air_conditioning_details = models.CharField(
        max_length=255,
        blank=True,
        help_text=(
            "Optional room-specific information, for example: "
            "'Air conditioning in all bedrooms and the main living room.'"
        ),
    )
    pool = models.CharField(
        max_length=20,
        choices=PoolType.choices,
        default=PoolType.NONE,
        help_text="Select the property's swimming-pool arrangement.",
    )
    pool_heated = models.BooleanField(
        default=False,
        help_text="Enable only when the swimming pool can be heated.",
    )
    pool_details = models.CharField(
        max_length=255,
        blank=True,
        help_text=(
            "Optional pool information, for example: "
            "'Private infinity pool open from May to October.'"
        ),
    )

    # Related services and public property highlights.
    services = models.ManyToManyField(
        Service,
        related_name="properties",
        blank=True,
    )
    amenities = models.ManyToManyField(
        PropertyAmenity,
        related_name="properties",
        blank=True,
        help_text=(
            "Optional public highlights such as Outdoor Dining, Pizza Oven, "
            "Landscaped Gardens or Pet Friendly. Recommended for rental "
            "properties."
        ),
    )
    show_property_highlights = models.BooleanField(
        default=False,
        help_text=(
            "Display air-conditioning, pool and selected amenity information "
            "on the public property page. Optional for managed-only homes and "
            "recommended for rental properties."
        ),
    )

    # Portfolio presentation.
    cover_image = models.ImageField(upload_to="properties/covers/")
    featured = models.BooleanField(default=False)
    featured_order = models.PositiveSmallIntegerField(
        default=0,
        help_text=(
            "Controls the order of featured properties. Lower numbers appear "
            "first."
        ),
    )
    published = models.BooleanField(default=True)

    # Rental information. Every property is managed by Oliverde; this flag
    # marks those that are additionally available for private rental.
    available_for_rental = models.BooleanField(
        default=False,
        help_text=(
            "Enable when this managed property is also available for private "
            "rental."
        ),
    )
    rental_banner_text = models.CharField(
        max_length=100,
        default="Available for Private Rental",
        blank=True,
        help_text=(
            "Banner displayed on rental properties. Leave blank to use the "
            "default wording."
        ),
    )
    rental_intro = models.TextField(
        blank=True,
        help_text=(
            "Optional introduction displayed near the rental enquiry area."
        ),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Properties"
        ordering = ["-featured", "featured_order", "title"]

    def clean(self):
        """Validate combinations that would otherwise be contradictory."""
        super().clean()
        errors = {}

        if self.pool == self.PoolType.NONE and self.pool_heated:
            errors["pool_heated"] = (
                "A property without a swimming pool cannot have a heated pool."
            )

        if (
            self.air_conditioning == self.AirConditioning.NONE
            and self.air_conditioning_details.strip()
        ):
            errors["air_conditioning_details"] = (
                "Remove the air-conditioning details or select an "
                "air-conditioning option."
            )

        if self.pool == self.PoolType.NONE and self.pool_details.strip():
            errors["pool_details"] = (
                "Remove the pool details or select a swimming-pool option."
            )

        if self.show_real_name_publicly and not self.title.strip():
            errors["title"] = "Enter the approved public property name."

        if errors:
            raise ValidationError(errors)

    @property
    def display_title(self):
        """Return the property name that is safe to display publicly."""
        if self.show_real_name_publicly:
            return self.title

        if self.public_title:
            return self.public_title

        return f"Private {self.get_property_type_display()}"

    @property
    def display_rental_banner(self):
        """Return the selected rental banner or its default wording."""
        return (
            self.rental_banner_text.strip()
            or "Available for Private Rental"
        )

    def get_absolute_url(self):
        return reverse(
            "portfolio:property_detail",
            kwargs={
                "slug": self.slug,
                "public_id": self.public_id,
            },
        )

    def __str__(self):
        # Django Admin continues to show the real internal name.
        return self.title


class PropertyImage(models.Model):
    """An ordered, categorised image in a property gallery."""

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
    image = models.ImageField(upload_to="properties/gallery/")
    section = models.CharField(
        max_length=20,
        choices=Section.choices,
        default=Section.EXTERIOR,
    )
    caption = models.CharField(max_length=255, blank=True)
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        help_text=(
            "Use a privacy-safe description. Do not include the real property "
            "name unless approved."
        ),
    )
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["section", "order", "pk"]

    def __str__(self):
        # Internal Admin references may use the real property title.
        return f"{self.property.title} — {self.get_section_display()}"


class Testimonial(models.Model):
    """An approved client testimonial."""

    quote = models.TextField()
    author_name = models.CharField(
        max_length=100,
        help_text=(
            "Use an approved public name, initials or anonymous label where "
            "discretion is required."
        ),
    )
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