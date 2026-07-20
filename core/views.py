from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from portfolio.models import Property, Testimonial

from .forms import ContactForm


class PrivacyPolicyView(TemplateView):
    template_name = "legal/privacy_policy.html"


class CookiePolicyView(TemplateView):
    template_name = "legal/cookie_policy.html"


class LegalNoticeView(TemplateView):
    template_name = "legal/legal_notice.html"


def custom_404(request, exception):
    """Render the custom 404 page."""
    return render(request, "404.html", status=404)


class RobotsView(TemplateView):
    """Serve the site's robots.txt file."""

    template_name = "robots.txt"
    content_type = "text/plain"


class HomeView(TemplateView):
    """Homepage."""

    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["featured_properties"] = Property.objects.filter(
            published=True,
            featured=True,
        )[:3]

        context["testimonials"] = Testimonial.objects.filter(
            featured_on_homepage=True,
        )[:4]

        return context


class AboutView(TemplateView):
    """About page."""

    template_name = "core/about.html"


class ContactView(FormView):
    """Contact page."""

    template_name = "core/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact")

    def form_valid(self, form):
        """
        Validate the contact form.

        MailerSend integration will be added once production
        API credentials have been configured.
        """

        # TODO:
        # Save the enquiry and send it through MailerSend once the
        # production integration has been configured.

        messages.success(
            self.request,
            "Thank you — your message has been received. "
            "We'll be in touch shortly.",
        )

        return super().form_valid(form)