from django.contrib import admin
from .models import Destination, Service, ServiceFeature, Property, PropertyImage, Testimonial


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3


class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 3


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("title", "destination", "property_type", "bedrooms", "featured", "published")
    list_filter = ("destination", "property_type", "featured", "published")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PropertyImageInline]
    filter_horizontal = ("services",)


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ServiceFeatureInline]


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("author_name", "destination", "property", "featured_on_homepage")
    list_filter = ("featured_on_homepage", "destination")