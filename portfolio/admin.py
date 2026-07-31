from django.contrib import admin

from .models import (
    Destination,
    Property,
    PropertyAmenity,
    PropertyImage,
    Service,
    ServiceFeature,
    ServiceImage,
    Testimonial,
)


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

    fields = (
        "image",
        "section",
        "caption",
        "alt_text",
        "order",
    )

    ordering = (
        "section",
        "order",
    )


class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 1

    fields = (
        "text",
        "order",
    )

    ordering = (
        "order",
    )


class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1

    fields = (
        "image",
        "caption",
        "alt_text",
        "order",
    )

    ordering = (
        "order",
    )


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "display_title",
        "title",
        "destination",
        "property_type",
        "bedrooms",
        "air_conditioning",
        "pool",
        "available_for_rental",
        "featured",
        "published",
    )

    list_filter = (
        "destination",
        "property_type",
        "air_conditioning",
        "pool",
        "pool_heated",
        "available_for_rental",
        "featured",
        "published",
    )

    search_fields = (
        "title",
        "public_title",
        "public_id",
        "slug",
        "description",
        "air_conditioning_details",
        "pool_details",
    )

    ordering = (
        "-featured",
        "featured_order",
        "title",
    )

    inlines = [
        PropertyImageInline,
    ]

    filter_horizontal = (
        "services",
        "amenities",
    )

    fieldsets = (
        (
            "Internal Information",
            {
                "fields": (
                    "title",
                    "destination",
                    "property_type",
                ),
                "description": (
                    "The internal title is visible in Django Admin but should "
                    "not be exposed publicly unless specifically approved."
                ),
            },
        ),
        (
            "Public Identity and Privacy",
            {
                "fields": (
                    "public_title",
                    "show_real_name_publicly",
                    "slug",
                    "public_id",
                    "description",
                    "cover_image",
                ),
                "description": (
                    "Use a privacy-safe public title and slug unless the owner "
                    "has approved publication of the property's real name."
                ),
            },
        ),
        (
            "Property Details",
            {
                "fields": (
                    "bedrooms",
                    "bathrooms",
                    "sleeps",
                    "land_size_hectares",
                ),
            },
        ),
        (
            "Air Conditioning",
            {
                "fields": (
                    "air_conditioning",
                    "air_conditioning_details",
                ),
            },
        ),
        (
            "Swimming Pool",
            {
                "fields": (
                    "pool",
                    "pool_heated",
                    "pool_details",
                ),
            },
        ),
        (
            "Services and Highlights",
            {
                "fields": (
                    "services",
                    "amenities",
                    "show_property_highlights",
                ),
            },
        ),
        (
            "Rental Information",
            {
                "fields": (
                    "available_for_rental",
                    "rental_banner_text",
                    "rental_intro",
                ),
            },
        ),
        (
            "Publication and Homepage",
            {
                "fields": (
                    "published",
                    "featured",
                    "featured_order",
                ),
            },
        ),
        (
            "Record Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": (
                    "collapse",
                ),
            },
        ),
    )

    readonly_fields = (
        "public_id",
        "created_at",
        "updated_at",
    )


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "tagline",
    )

    search_fields = (
        "name",
        "tagline",
        "description",
    )

    prepopulated_fields = {
        "slug": (
            "name",
        ),
    }


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
    )

    search_fields = (
        "title",
        "description",
    )

    prepopulated_fields = {
        "slug": (
            "title",
        ),
    }

    inlines = [
        ServiceFeatureInline,
        ServiceImageInline,
    ]


@admin.register(PropertyAmenity)
class PropertyAmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "order",
    )

    list_filter = (
        "category",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "category",
        "order",
        "name",
    )

    list_editable = (
        "order",
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        "author_name",
        "destination",
        "property",
        "featured_on_homepage",
    )

    list_filter = (
        "featured_on_homepage",
        "destination",
    )

    search_fields = (
        "author_name",
        "quote",
        "property__title",
        "property__public_title",
    )