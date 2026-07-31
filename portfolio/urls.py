from django.urls import path

from . import views

app_name = "portfolio"

urlpatterns = [
    path(
        "",
        views.PortfolioLandingView.as_view(),
        name="list",
    ),
    path(
        "properties/",
        views.PropertyListAllView.as_view(),
        name="all_properties",
    ),
    path(
        "destination/<slug:slug>/",
        views.DestinationDetailView.as_view(),
        name="destination_detail",
    ),
    path(
        "properties/<slug:slug>/<uuid:public_id>/",
        views.PropertyDetailView.as_view(),
        name="property_detail",
    ),
]