from django.views.generic import DetailView, ListView

from journal.models import JournalPost
from portfolio.models import Service

from .content import COMMON_FAQS, SERVICE_CONTENT


class ServiceListView(ListView):
    model = Service
    template_name = "services/list.html"
    context_object_name = "services"

    def get_queryset(self):
        return Service.objects.prefetch_related(
            "features",
            "gallery",
        )


class ServiceDetailView(DetailView):
    model = Service
    template_name = "services/detail.html"
    context_object_name = "service"

    def get_queryset(self):
        return Service.objects.prefetch_related(
            "features",
            "gallery",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["related_properties"] = (
            self.object.properties
            .filter(published=True)
            .select_related("destination")
            [:3]
        )

        # Extra editorial sections live in services/content.py (no database).
        extra = SERVICE_CONTENT.get(self.object.slug)

        context["extra"] = extra
        context["faqs"] = COMMON_FAQS if extra else []
        context["related_articles"] = []

        if extra and extra.get("articles"):
            context["related_articles"] = JournalPost.objects.filter(
                is_published=True,
                slug__in=extra["articles"],
            )[:3]

        return context