"""
URL configuration for the Oliverde project.

The `urlpatterns` list routes URLs to views.
"""

from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from core.views import (
    AboutView,
    ContactView,
    HomeView,
    RobotsView,
)
from .sitemaps import (
    DestinationSitemap,
    PropertySitemap,
    ServiceSitemap,
    StaticViewSitemap,
)


sitemaps = {
    "static": StaticViewSitemap,
    "properties": PropertySitemap,
    "destinations": DestinationSitemap,
    "services": ServiceSitemap,
}


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", ContactView.as_view(), name="contact"),

    path("portfolio/", include("portfolio.urls")),
    path("services/", include("services.urls")),

    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="sitemap",
    ),

    path(
        "robots.txt",
        RobotsView.as_view(),
        name="robots",
    ),
]


handler404 = "core.views.custom_404"