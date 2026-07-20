from django.urls import path
from . import views

app_name = "journal"

urlpatterns = [
    path("", views.JournalListView.as_view(), name="list"),
    path("<slug:slug>/", views.JournalDetailView.as_view(), name="detail"),
]