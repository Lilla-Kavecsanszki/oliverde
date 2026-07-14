"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views.
"""

from django.contrib import admin
from django.urls import include, path

from core.views import AboutView, HomeView, ContactView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path('contact/', ContactView.as_view(), name='contact'),
    path("portfolio/", include("portfolio.urls")),
    path("services/", include("services.urls")),
]