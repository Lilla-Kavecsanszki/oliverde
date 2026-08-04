from django.db.models import Case, IntegerField, Prefetch, When
from django.shortcuts import get_object_or_404, redirect
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
            .select_related("destination")
            .order_by(
                "featured_order",
                "public_title",
                "title",
            )[:6]
        )

        return context


class PropertyCollectionView(ListView):
    """
    Base property-grid view.

    Subclasses may apply additional restrictions, such as displaying only
    properties that are available for private rental.
    """

    model = Property
    template_name = "portfolio/property_list.html"
    context_object_name = "properties"
    paginate_by = 12

    page_title = "Our Collection"
    page_eyebrow = "Portfolio"
    page_description = (
        "A considered collection of private estates, villas and country "
        "homes managed by Oliverde across Tuscany, Umbria and Lazio."
    )
    collection_type = "all"

    allowed_sort_options = {
        "featured": (
            "-featured",
            "featured_order",
            "public_title",
            "title",
        ),
        "name": (
            "public_title",
            "title",
        ),
        "-name": (
            "-public_title",
            "-title",
        ),
        "destination": (
            "destination__name",
            "public_title",
            "title",
        ),
    }

    def get_base_queryset(self):
        """Return the initial published-property queryset."""
        return (
            Property.objects
            .filter(published=True)
            .select_related("destination")
        )

    def apply_collection_filter(self, queryset):
        """
        Apply collection-specific filtering.

        The default collection contains every published property managed by
        Oliverde.
        """
        return queryset

    def get_queryset(self):
        queryset = self.apply_collection_filter(
            self.get_base_queryset()
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
                destination__slug=destination_slug,
            )

        ordering = self.allowed_sort_options.get(
            sort_option,
            self.allowed_sort_options["featured"],
        )

        return queryset.order_by(*ordering)

    def get_available_destinations(self):
        """
        Return destinations represented in the current collection.

        The rental page therefore lists only destinations that contain at
        least one published rental property.
        """
        property_queryset = self.apply_collection_filter(
            Property.objects.filter(published=True)
        )

        return (
            Destination.objects
            .filter(
                properties__in=property_queryset,
            )
            .distinct()
            .order_by("name")
        )

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

        context["destinations"] = self.get_available_destinations()
        context["selected_destination"] = selected_destination
        context["selected_sort"] = selected_sort

        context["page_title"] = self.page_title
        context["page_eyebrow"] = self.page_eyebrow
        context["page_description"] = self.page_description
        context["collection_type"] = self.collection_type

        query_parameters = self.request.GET.copy()
        query_parameters.pop("page", None)

        context["pagination_query"] = query_parameters.urlencode()

        return context


class PropertyListAllView(PropertyCollectionView):
    """Display every published property managed by Oliverde."""

    page_title = "Our Collection"
    page_eyebrow = "Homes Under Our Care"
    page_description = (
        "A considered collection of private estates, villas and country "
        "homes managed by Oliverde across Tuscany, Umbria and Lazio."
    )
    collection_type = "all"


class HolidayRentalListView(PropertyCollectionView):
    """Display published managed properties available for private rental."""

    page_title = "Holiday Rentals"
    page_eyebrow = "Stay with Oliverde"
    page_description = (
        "Discover a private selection of homes under Oliverde's care that "
        "are also available for exceptional stays in Italy."
    )
    collection_type = "rentals"

    def apply_collection_filter(self, queryset):
        return queryset.filter(
            available_for_rental=True,
        )


class DestinationDetailView(DetailView):
    """A destination page with its published properties."""

    model = Destination
    template_name = "portfolio/destination_detail.html"
    context_object_name = "destination"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["properties"] = (
            self.object.properties
            .filter(published=True)
            .select_related("destination")
            .order_by(
                "-featured",
                "featured_order",
                "public_title",
                "title",
            )
        )

        context["testimonial"] = (
            Testimonial.objects
            .filter(destination=self.object)
            .first()
        )

        return context


class PropertyDetailView(DetailView):
    """A public property page identified securely by its UUID."""

    model = Property
    template_name = "portfolio/property_detail.html"
    context_object_name = "property"

    def get_queryset(self):
        """
        Return published properties with related content prefetched.

        Gallery categories remain available in the CMS and determine the
        editorial image order, but the public template displays the images
        as one continuous gallery.
        """
        gallery_queryset = (
            PropertyImage.objects
            .annotate(
                section_position=Case(
                    When(section="arrival", then=0),
                    When(section="exterior", then=1),
                    When(section="living", then=2),
                    When(section="bedrooms", then=3),
                    When(section="outdoors", then=4),
                    When(section="gardens", then=5),
                    When(section="details", then=6),
                    When(section="views", then=7),
                    default=99,
                    output_field=IntegerField(),
                )
            )
            .order_by(
                "section_position",
                "order",
                "pk",
            )
        )

        return (
            Property.objects
            .filter(published=True)
            .select_related("destination")
            .prefetch_related(
                Prefetch(
                    "gallery",
                    queryset=gallery_queryset,
                ),
                "services",
                "amenities",
            )
        )

    def get_object(self, queryset=None):
        """
        Retrieve the property using its random public UUID.

        The slug is deliberately not used for the database lookup.
        """
        queryset = queryset or self.get_queryset()

        return get_object_or_404(
            queryset,
            public_id=self.kwargs["public_id"],
        )

    def get(self, request, *args, **kwargs):
        """
        Redirect an incorrect or outdated slug to the canonical URL.

        The UUID remains stable even when the editorial slug changes.
        """
        self.object = self.get_object()

        if kwargs.get("slug") != self.object.slug:
            return redirect(
                self.object.get_absolute_url(),
                permanent=True,
            )

        context = self.get_context_data(
            object=self.object,
        )

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["gallery"] = list(
            self.object.gallery.all()
        )

        context["services"] = (
            self.object.services.all()
        )

        context["amenities"] = (
            self.object.amenities.all()
        )

        context["related_properties"] = (
            Property.objects
            .filter(
                destination=self.object.destination,
                published=True,
            )
            .exclude(pk=self.object.pk)
            .select_related("destination")
            .order_by(
                "-featured",
                "featured_order",
                "public_title",
                "title",
            )[:3]
        )

        return context