from django.views.generic import ListView
from portfolio.models import Service


class ServiceListView(ListView):
    model = Service
    template_name = "services/list.html"
    context_object_name = "services"

    def get_queryset(self):
        return Service.objects.prefetch_related("features")