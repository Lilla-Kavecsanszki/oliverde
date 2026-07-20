from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from journal.models import JournalPost
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
            "privacy_policy",
            "cookie_policy",
            "legal_notice",
        ]

    def location(self, item):
        return reverse(item)


class PropertySitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return (
            Property.objects
            .filter(published=True)
            .order_by("-updated_at")
        )

    def lastmod(self, obj):
        return obj.updated_at


class DestinationSitemap(Sitemap):
    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return (
            Destination.objects
            .filter(properties__published=True)
            .distinct()
            .order_by("name")
        )

    def lastmod(self, obj):
        latest = (
            obj.properties
            .filter(published=True)
            .order_by("-updated_at")
            .first()
        )
        return latest.updated_at if latest else None


class ServiceSitemap(Sitemap):
    priority = 0.6
    changefreq = "monthly"

    def items(self):
        return Service.objects.all()

    # Uncomment if your Service model has an updated_at field.
    #
    # def lastmod(self, obj):
    #     return obj.updated_at


class JournalSitemap(Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return (
            JournalPost.objects
            .filter(is_published=True)
            .order_by("-published_at")
        )

    def lastmod(self, obj):
        return obj.updated_at