from django.urls import path

from .views import ContactView, HomeView, AboutView

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path('contact/', ContactView.as_view(), name='contact'),
]