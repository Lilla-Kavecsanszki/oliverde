import logging
import smtplib

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.utils import timezone
from django.utils.html import escape

from .models import ContactEnquiry


logger = logging.getLogger(__name__)


class ContactEmailError(Exception):
    """Raised when an enquiry notification cannot be delivered."""


def build_admin_url(enquiry):
    """Return the production admin URL for an enquiry."""
    path = reverse(
        "admin:core_contactenquiry_change",
        args=[enquiry.pk],
    )

    site_url = settings.SITE_URL.rstrip("/")

    return f"{site_url}{path}"


def send_contact_enquiry_notification(enquiry):
    """
    Notify Oliverde about a saved contact enquiry.

    The enquiry must already exist in the database before this function
    is called.
    """
    if not settings.DEFAULT_FROM_EMAIL:
        raise ContactEmailError(
            "The sender email address is not configured."
        )

    if not settings.CONTACT_RECIPIENT_EMAIL:
        raise ContactEmailError(
            "The contact recipient email address is not configured."
        )

    property_label = (
        enquiry.property.display_title
        if enquiry.property
        else "Not specified"
    )

    subject = (
        "New Oliverde website enquiry — "
        f"{enquiry.get_enquiry_type_display()}"
    )

    admin_url = build_admin_url(enquiry)

    text_body = "\n".join(
        [
            "A new enquiry has been received through the Oliverde website.",
            "",
            f"Name: {enquiry.name}",
            f"Email: {enquiry.email}",
            f"Phone: {enquiry.phone or 'Not provided'}",
            (
                "Enquiry type: "
                f"{enquiry.get_enquiry_type_display()}"
            ),
            f"Property: {property_label}",
            "",
            "Message:",
            enquiry.message,
            "",
            f"View in Django Admin: {admin_url}",
        ]
    )

    html_body = f"""
        <h2>New Oliverde website enquiry</h2>

        <table
            cellpadding="8"
            cellspacing="0"
            style="border-collapse:collapse;"
        >
            <tr>
                <th align="left">Name</th>
                <td>{escape(enquiry.name)}</td>
            </tr>
            <tr>
                <th align="left">Email</th>
                <td>{escape(enquiry.email)}</td>
            </tr>
            <tr>
                <th align="left">Phone</th>
                <td>{escape(enquiry.phone or "Not provided")}</td>
            </tr>
            <tr>
                <th align="left">Enquiry type</th>
                <td>
                    {escape(enquiry.get_enquiry_type_display())}
                </td>
            </tr>
            <tr>
                <th align="left">Property</th>
                <td>{escape(property_label)}</td>
            </tr>
        </table>

        <h3>Message</h3>

        <div style="white-space:pre-line;">
            {escape(enquiry.message)}
        </div>

        <p style="margin-top:24px;">
            <a href="{escape(admin_url)}">
                View this enquiry in Django Admin
            </a>
        </p>
    """

    email_message = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.CONTACT_RECIPIENT_EMAIL],
        reply_to=[enquiry.email],
    )

    email_message.attach_alternative(
        html_body,
        "text/html",
    )

    try:
        sent_count = email_message.send(
            fail_silently=False,
        )
    except (
        smtplib.SMTPException,
        ConnectionError,
        TimeoutError,
        OSError,
    ) as exc:
        enquiry.email_status = ContactEnquiry.EmailStatus.FAILED
        enquiry.email_error = (
            f"{exc.__class__.__name__}: "
            f"{str(exc)[:400]}"
        )
        enquiry.save(
            update_fields=(
                "email_status",
                "email_error",
                "updated_at",
            )
        )

        logger.exception(
            "Contact enquiry notification failed. Enquiry ID: %s",
            enquiry.pk,
        )

        raise ContactEmailError(
            "The enquiry notification could not be delivered."
        ) from exc

    if sent_count != 1:
        enquiry.email_status = ContactEnquiry.EmailStatus.FAILED
        enquiry.email_error = (
            "The email backend returned an unexpected send count."
        )
        enquiry.save(
            update_fields=(
                "email_status",
                "email_error",
                "updated_at",
            )
        )

        logger.error(
            "Unexpected contact email send count. "
            "Enquiry ID: %s, count: %s",
            enquiry.pk,
            sent_count,
        )

        raise ContactEmailError(
            "The email backend did not confirm delivery."
        )

    enquiry.email_status = ContactEnquiry.EmailStatus.SENT
    enquiry.email_sent_at = timezone.now()
    enquiry.email_error = ""
    enquiry.save(
        update_fields=(
            "email_status",
            "email_sent_at",
            "email_error",
            "updated_at",
        )
    )

    logger.info(
        "Contact enquiry notification sent. Enquiry ID: %s",
        enquiry.pk,
    )