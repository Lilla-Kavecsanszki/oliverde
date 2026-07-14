from django.contrib import admin

from .models import (
    Destination,
    Property,
    PropertyImage,
    Service,
    ServiceFeature,
    Testimonial,
)


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3
    fields = ("image", "caption", "order")
    ordering = ("order",)


class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 3
    fields = ("text", "order")
    ordering = ("order",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ServiceFeatureInline]


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "destination",
        "property_type",
        "bedrooms",
        "featured",
        "published",
        "updated_at",
    )
    list_filter = (
        "destination",
        "property_type",
        "featured",
        "published",
    )
    search_fields = (
        "title",
        "description",
        "destination__name",
    )
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("services",)
    inlines = [PropertyImageInline]
    readonly_fields = ("created_at", "updated_at")


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "tagline", "description")
    prepopulated_fields = {"slug": ("name",)}


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
    )