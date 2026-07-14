from django.views.generic import TemplateView
from portfolio.models import Property, Testimonial


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_properties"] = Property.objects.filter(
            published=True, featured=True
        )[:3]
        context["testimonials"] = Testimonial.objects.filter(
            featured_on_homepage=True
        )[:4]
        return context


class AboutView(TemplateView):
    template_name = "core/about.html"