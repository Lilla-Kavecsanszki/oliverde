from django.views.generic import ListView, DetailView
from portfolio.models import Service


class ServiceListView(ListView):
    model = Service
    template_name = "services/list.html"
    context_object_name = "services"

    def get_queryset(self):
        return Service.objects.prefetch_related("features")


class ServiceDetailView(DetailView):
    model = Service
    template_name = "services/detail.html"
    context_object_name = "service"

    def get_queryset(self):
        return Service.objects.prefetch_related("features")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_properties"] = self.object.properties.filter(
            published=True
        )[:3]
        return context