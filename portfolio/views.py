from django.views.generic import ListView, DetailView
from .models import Destination, Property, Testimonial


class PortfolioLandingView(ListView):
    """The Portfolio page: browse-by-destination grid + featured properties."""
    model = Destination
    template_name = "portfolio/list.html"
    context_object_name = "destinations"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_properties"] = Property.objects.filter(
            published=True, featured=True
        )[:6]
        return context


class PropertyListAllView(ListView):
    """The full property grid — 'View all properties'."""
    model = Property
    template_name = "portfolio/property_list.html"
    context_object_name = "properties"
    paginate_by = 12

    def get_queryset(self):
        return Property.objects.filter(published=True)


class DestinationDetailView(DetailView):
    model = Destination
    template_name = "portfolio/destination_detail.html"
    context_object_name = "destination"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["properties"] = self.object.properties.filter(published=True)
        context["testimonial"] = Testimonial.objects.filter(
            destination=self.object
        ).first()
        return context


class PropertyDetailView(DetailView):
    model = Property
    template_name = "portfolio/property_detail.html"
    context_object_name = "property"

    def get_queryset(self):
        return Property.objects.filter(published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["gallery"] = self.object.gallery.all()
        context["services"] = self.object.services.all()
        context["related_properties"] = Property.objects.filter(
            destination=self.object.destination, published=True
        ).exclude(pk=self.object.pk)[:3]
        return context