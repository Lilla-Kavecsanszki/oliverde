"""Shared helpers for the project's tests."""

from django.test import override_settings

from portfolio.models import Destination, Property, Service

# Keep tests independent of Cloudinary, WhiteNoise manifests and HTTPS.
site_test_settings = override_settings(
    SECURE_SSL_REDIRECT=False,
    ALLOWED_HOSTS=["testserver"],
    STORAGES={
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": (
                "django.contrib.staticfiles.storage.StaticFilesStorage"
            ),
        },
    },
)


def make_destination(name="Cortona", slug="cortona"):
    destination, _ = Destination.objects.get_or_create(
        slug=slug,
        defaults={
            "name": name,
            "cover_image": "destinations/test.jpg",
        },
    )
    return destination


def make_service(title="Property Maintenance", slug="property-maintenance"):
    return Service.objects.create(
        title=title,
        slug=slug,
        description="Regular care of your home.",
    )


def make_property(destination=None, **overrides):
    values = {
        "title": "Internal Farmhouse Name",
        "slug": "olive-grove-house",
        "destination": destination or make_destination(),
        "property_type": Property.PropertyType.FARMHOUSE,
        "description": "A quiet stone farmhouse.",
        "cover_image": "properties/covers/test.jpg",
    }
    values.update(overrides)
    return Property.objects.create(**values)
