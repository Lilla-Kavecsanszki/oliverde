from collections import OrderedDict

from django.db.models import Prefetch
from django.views.generic import DetailView, ListView

from .models import (
    Destination,
    Property,
    PropertyImage,
    Testimonial,
)


class PortfolioLandingView(ListView):
    """Portfolio landing page with destinations and featured properties."""

    model = Destination
    template_name = "portfolio/list.html"
    context_object_name = "destinations"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["featured_properties"] = (
            Property.objects
            .filter(
                published=True,
                featured=True,
            )
            .select_related("destination")[:6]
        )

        return context


class PropertyListAllView(ListView):
    """Full property grid with destination filtering and sorting."""

    model = Property
    template_name = "portfolio/property_list.html"
    context_object_name = "properties"
    paginate_by = 12

    allowed_sort_options = {
        "featured": ("-featured", "title"),
        "name": ("title",),
        "-name": ("-title",),
        "destination": ("destination__name", "title"),
    }

    def get_queryset(self):
        queryset = (
            Property.objects
            .filter(published=True)
            .select_related("destination")
        )

        destination_slug = self.request.GET.get(
            "destination",
            "",
        ).strip()

        sort_option = self.request.GET.get(
            "sort",
            "featured",
        ).strip()

        if destination_slug:
            queryset = queryset.filter(
                destination__slug=destination_slug
            )

        ordering = self.allowed_sort_options.get(
            sort_option,
            self.allowed_sort_options["featured"],
        )

        return queryset.order_by(*ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        selected_destination = self.request.GET.get(
            "destination",
            "",
        ).strip()

        selected_sort = self.request.GET.get(
            "sort",
            "featured",
        ).strip()

        if selected_sort not in self.allowed_sort_options:
            selected_sort = "featured"

        context["destinations"] = (
            Destination.objects
            .filter(properties__published=True)
            .distinct()
            .order_by("name")
        )

        context["selected_destination"] = selected_destination
        context["selected_sort"] = selected_sort

        query_parameters = self.request.GET.copy()
        query_parameters.pop("page", None)

        context["pagination_query"] = query_parameters.urlencode()

        return context


class DestinationDetailView(DetailView):
    model = Destination
    template_name = "portfolio/destination_detail.html"
    context_object_name = "destination"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["properties"] = (
            self.object.properties
            .filter(published=True)
            .select_related("destination")
        )

        context["testimonial"] = (
            Testimonial.objects
            .filter(destination=self.object)
            .first()
        )

        return context


class PropertyDetailView(DetailView):
    model = Property
    template_name = "portfolio/property_detail.html"
    context_object_name = "property"

    def get_queryset(self):
        return (
            Property.objects
            .filter(published=True)
            .select_related("destination")
            .prefetch_related(
                Prefetch(
                    "gallery",
                    queryset=PropertyImage.objects.order_by(
                        "section",
                        "order",
                        "pk",
                    ),
                ),
                "services",
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        gallery_images = list(self.object.gallery.all())
        gallery_sections = OrderedDict()

        editorial_titles = {
            "arrival": "Arrival",
            "exterior": "The House",
            "living": "Living Spaces",
            "bedrooms": "Private Retreats",
            "outdoors": "Outdoor Living",
            "gardens": "Gardens & Grounds",
            "details": "Architectural Details",
            "views": "Views",
        }

        section_labels = dict(PropertyImage.Section.choices)

        for image in gallery_images:

            if image.section not in gallery_sections:
                gallery_sections[image.section] = {
                    "key": image.section,
                    "title": editorial_titles.get(
                        image.section,
                        section_labels.get(
                            image.section,
                            image.section.title(),
                        ),
                    ),
                    "images": [],
                }

            gallery_sections[image.section]["images"].append(image)

        context["gallery"] = gallery_images
        context["gallery_sections"] = list(
            gallery_sections.values()
        )

        context["services"] = self.object.services.all()

        context["related_properties"] = (
            Property.objects
            .filter(
                destination=self.object.destination,
                published=True,
            )
            .exclude(pk=self.object.pk)
            .select_related("destination")
            .order_by("-featured", "title")[:3]
        )

        return context