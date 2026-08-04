from django.contrib import admin

from .models import ContactEnquiry


@admin.register(ContactEnquiry)
class ContactEnquiryAdmin(admin.ModelAdmin):
    """Admin inbox for public website enquiries."""

    list_display = (
        "name",
        "email",
        "enquiry_type",
        "property",
        "status",
        "email_status",
        "submitted_at",
    )

    list_filter = (
        "status",
        "email_status",
        "enquiry_type",
        "submitted_at",
    )

    search_fields = (
        "name",
        "email",
        "phone",
        "property__title",
        "property__public_title",
        "message",
    )

    ordering = ("-submitted_at",)

    date_hierarchy = "submitted_at"

    readonly_fields = (
        "name",
        "email",
        "phone",
        "enquiry_type",
        "property",
        "message",
        "email_status",
        "email_error",
        "submitted_at",
        "updated_at",
        "email_sent_at",
    )

    fieldsets = (
        (
            "Enquiry",
            {
                "fields": (
                    "name",
                    "email",
                    "phone",
                    "enquiry_type",
                    "property",
                    "message",
                ),
            },
        ),
        (
            "Oliverde workflow",
            {
                "fields": (
                    "status",
                    "internal_notes",
                ),
            },
        ),
        (
            "Notification delivery",
            {
                "fields": (
                    "email_status",
                    "email_sent_at",
                    "email_error",
                ),
            },
        ),
        (
            "Record information",
            {
                "fields": (
                    "submitted_at",
                    "updated_at",
                ),
            },
        ),
    )

    def has_add_permission(self, request):
        """Enquiries should originate from the public form."""
        return False