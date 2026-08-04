from django.db import models

from portfolio.models import Property


class ContactEnquiry(models.Model):
    """A public enquiry submitted through the Oliverde website."""

    class EnquiryType(models.TextChoices):
        GENERAL = "general", "General enquiry"
        MANAGEMENT = "management", "Property management services"
        RENTAL = "rental", "Holiday rental enquiry"
        RESTORATION = "restoration", "Restoration management"
        POST_PURCHASE = "post_purchase", "Post-purchase support"
        OTHER = "other", "Something else"

    class Status(models.TextChoices):
        NEW = "new", "New"
        IN_PROGRESS = "in_progress", "In progress"
        REPLIED = "replied", "Replied"
        CLOSED = "closed", "Closed"
        SPAM = "spam", "Spam"

    class EmailStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        SENT = "sent", "Sent"
        FAILED = "failed", "Failed"

    name = models.CharField(
        max_length=100,
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=30,
        blank=True,
    )

    enquiry_type = models.CharField(
        max_length=30,
        choices=EnquiryType.choices,
        default=EnquiryType.GENERAL,
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contact_enquiries",
        help_text=(
            "The related Oliverde property, when the enquiry originated "
            "from a property page."
        ),
    )

    message = models.TextField(
        max_length=5000,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )

    email_status = models.CharField(
        max_length=20,
        choices=EmailStatus.choices,
        default=EmailStatus.PENDING,
        editable=False,
    )

    email_error = models.CharField(
        max_length=500,
        blank=True,
        editable=False,
        help_text=(
            "Internal delivery information. Never display this publicly."
        ),
    )

    internal_notes = models.TextField(
        blank=True,
        help_text=(
            "Private notes visible only to authorised Oliverde staff."
        ),
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    email_sent_at = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
    )

    class Meta:
        ordering = ("-submitted_at",)
        verbose_name = "contact enquiry"
        verbose_name_plural = "contact enquiries"

    def __str__(self):
        return (
            f"{self.name} — "
            f"{self.get_enquiry_type_display()} — "
            f"{self.submitted_at:%d %b %Y}"
        )