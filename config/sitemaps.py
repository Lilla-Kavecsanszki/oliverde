from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from portfolio.models import Destination, Property, Service


class StaticViewSitemap(Sitemap):
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return [
            "home",
            "about",
            "contact",
            "portfolio:list",
            "portfolio:all_properties",
            "services:list",
        ]

    def location(self, item):
        return reverse(item)


class PropertySitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return Property.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.updated_at


class DestinationSitemap(Sitemap):
    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return Destination.objects.all()

    def lastmod(self, obj):
        latest = obj.properties.filter(published=True).order_by("-updated_at").first()
        return latest.updated_at if latest else None


class ServiceSitemap(Sitemap):
    priority = 0.6
    changefreq = "monthly"

    def items(self):
        return Service.objects.all()