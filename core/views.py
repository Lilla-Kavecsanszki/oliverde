import logging
from uuid import UUID

from django.conf import settings
from django.contrib import messages
from django.db import DatabaseError
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from portfolio.models import Property, Testimonial

from .email import (
    ContactEmailError,
    send_contact_enquiry_notification,
)
from .forms import ContactForm
from .models import ContactEnquiry
from .security import (
    RateLimitExceeded,
    TurnstileUnavailableError,
    enforce_contact_rate_limit,
    verify_turnstile,
)


logger = logging.getLogger(__name__)


class PrivacyPolicyView(TemplateView):
    """Display the Privacy Policy."""

    template_name = "legal/privacy_policy.html"


class CookiePolicyView(TemplateView):
    """Display the Cookie Policy."""

    template_name = "legal/cookie_policy.html"


class LegalNoticeView(TemplateView):
    """Display the Legal Notice."""

    template_name = "legal/legal_notice.html"


def custom_404(request, exception):
    """Render the custom 404 page."""
    return render(
        request,
        "404.html",
        status=404,
    )


class RobotsView(TemplateView):
    """Serve the site's robots.txt file."""

    template_name = "robots.txt"
    content_type = "text/plain"


class HomeView(TemplateView):
    """Display the homepage."""

    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["featured_properties"] = (
            Property.objects
            .filter(
                published=True,
                featured=True,
            )
            .select_related("destination")
            .order_by("title")[:4]
        )

        context["testimonials"] = (
            Testimonial.objects
            .filter(featured_on_homepage=True)[:4]
        )

        return context


class AboutView(TemplateView):
    """Display the About page."""

    template_name = "core/about.html"


class ContactView(FormView):
    """Display and process the public enquiry form."""

    template_name = "core/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact")

    def get_requested_rental_property(self):
        """
        Return the rental property referenced by the URL, when valid.

        The public UUID is accepted only when it belongs to a published
        property that is currently available for private rental.
        """
        if hasattr(self, "_requested_rental_property"):
            return self._requested_rental_property

        property_reference = self.request.GET.get(
            "property",
            "",
        ).strip()

        if not property_reference:
            self._requested_rental_property = None
            return None

        try:
            public_id = UUID(property_reference)
        except (TypeError, ValueError, AttributeError):
            self._requested_rental_property = None
            return None

        self._requested_rental_property = (
            Property.objects
            .filter(
                public_id=public_id,
                published=True,
                available_for_rental=True,
            )
            .select_related("destination")
            .first()
        )

        return self._requested_rental_property

    def get_initial(self):
        """
        Pre-fill enquiries initiated from a published rental property.

        Managed-only properties are deliberately ignored and cannot be
        attached through a manipulated URL.
        """
        initial = super().get_initial()
        property_obj = self.get_requested_rental_property()

        if property_obj:
            initial.update(
                {
                    "property_id": property_obj.public_id,
                    "enquiry_type": (
                        ContactEnquiry.EnquiryType.RENTAL
                    ),
                    "message": (
                        "I would like to enquire about staying at "
                        f"{property_obj.display_title}."
                    ),
                }
            )

        return initial

    def get_context_data(self, **kwargs):
        """Add Turnstile and rental-property context to the page."""
        context = super().get_context_data(**kwargs)

        context["turnstile_site_key"] = (
            settings.TURNSTILE_SITE_KEY
        )

        selected_property = self.get_requested_rental_property()
        form = context.get("form")

        if (
            selected_property is None
            and form is not None
            and form.is_bound
        ):
            property_reference = form.data.get(
                "property_id",
                "",
            ).strip()

            try:
                public_id = UUID(property_reference)
            except (TypeError, ValueError, AttributeError):
                public_id = None

            if public_id:
                selected_property = (
                    Property.objects
                    .filter(
                        public_id=public_id,
                        published=True,
                        available_for_rental=True,
                    )
                    .select_related("destination")
                    .first()
                )

        context["selected_property"] = selected_property

        return context

    def form_valid(self, form):
        """
        Securely process a validated public enquiry.

        The security challenge and rate limit are checked before the
        enquiry is saved. The database record is then created before
        Gmail notification is attempted.
        """
        try:
            turnstile_valid = verify_turnstile(
                self.request,
            )
        except TurnstileUnavailableError:
            logger.exception(
                "Contact-form security verification was unavailable."
            )

            form.add_error(
                None,
                (
                    "We could not complete the security check just now. "
                    "Your form has been preserved. Please wait a moment "
                    "and try again."
                ),
            )

            messages.error(
                self.request,
                "We could not verify your submission at this time.",
            )

            return super().form_invalid(form)

        if not turnstile_valid:
            form.add_error(
                None,
                (
                    "We could not verify this submission. Please complete "
                    "the security check again and resend your enquiry."
                ),
            )

            messages.error(
                self.request,
                (
                    "Please complete the security check before sending "
                    "your enquiry."
                ),
            )

            return super().form_invalid(form)

        try:
            enforce_contact_rate_limit(
                self.request,
            )
        except RateLimitExceeded:
            form.add_error(
                None,
                (
                    "For security reasons, we have temporarily limited "
                    "new enquiries from this connection. Please try again "
                    "later, or contact Oliverde directly by email or "
                    "telephone if your enquiry is urgent."
                ),
            )

            messages.warning(
                self.request,
                (
                    "This enquiry could not be submitted because the "
                    "security limit has been reached."
                ),
            )

            return super().form_invalid(form)

        property_obj = form.get_property()

        try:
            enquiry = ContactEnquiry.objects.create(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                phone=form.cleaned_data["phone"],
                enquiry_type=(
                    form.cleaned_data["enquiry_type"]
                ),
                property=property_obj,
                message=form.cleaned_data["message"],
            )
        except DatabaseError:
            logger.exception(
                "A contact enquiry could not be saved."
            )

            form.add_error(
                None,
                (
                    "We are sorry, but your enquiry could not be recorded "
                    "just now. Your form has been preserved. Please try "
                    "again shortly or contact Oliverde directly."
                ),
            )

            messages.error(
                self.request,
                "We could not safely record your enquiry.",
            )

            return super().form_invalid(form)

        try:
            send_contact_enquiry_notification(
                enquiry,
            )
        except ContactEmailError:
            logger.warning(
                "Contact enquiry saved but notification failed. "
                "Enquiry ID: %s",
                enquiry.pk,
            )

            messages.warning(
                self.request,
                (
                    "Thank you. Your enquiry has been safely received "
                    "and recorded in our system. Our email notification "
                    "is temporarily unavailable, but your message has "
                    "not been lost and remains available to the "
                    "Oliverde team."
                ),
            )

            return super().form_valid(form)

        messages.success(
            self.request,
            (
                "Thank you for getting in touch. Your enquiry has been "
                "received safely, and a member of the Oliverde team will "
                "review it shortly. We typically respond within one "
                "business day."
            ),
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        """Display a friendly summary for invalid submissions."""
        if form.errors.get("property_id"):
            form.add_error(
                None,
                (
                    "The selected property cannot accept private rental "
                    "enquiries."
                ),
            )

        messages.error(
            self.request,
            (
                "Please review the highlighted fields and try again. "
                "The information you entered has been preserved."
            ),
        )

        return super().form_invalid(form)