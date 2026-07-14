from django.views.generic import TemplateView, FormView
from django.contrib import messages
from django.urls import reverse_lazy
from portfolio.models import Property, Testimonial
from .forms import ContactForm


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


class ContactView(FormView):
    template_name = "core/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact")

    def form_valid(self, form):
        # TODO: wire up MailerSend here once API credentials are in .env.
        # For now this validates and confirms — no email is actually sent yet.
        #
        # Example once MailerSend is configured:
        # from mailersend import emails
        # mailer = emails.NewEmail(os.environ.get("MAILERSEND_API_KEY"))
        # mail_body = {}
        # mailer.set_mail_from({"email": "hello@oliverde.com"}, mail_body)
        # mailer.set_mail_to([{"email": "hello@oliverde.com"}], mail_body)
        # mailer.set_subject(f"New enquiry from {form.cleaned_data['name']}", mail_body)
        # mailer.set_plaintext_content(form.cleaned_data['message'], mail_body)
        # mailer.send(mail_body)

        messages.success(
            self.request,
            "Thank you — your message has been received. We'll be in touch shortly."
        )
        return super().form_valid(form)