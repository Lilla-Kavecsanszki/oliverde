import re

from django import forms

from portfolio.models import Property

from .models import ContactEnquiry


class ContactForm(forms.Form):
    """Public enquiry form for prospective clients and guests."""

    name = forms.CharField(
        label="Full name",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Your full name",
                "autocomplete": "name",
            }
        ),
    )

    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "your@email.com",
                "autocomplete": "email",
            }
        ),
    )

    phone = forms.CharField(
        label="Phone",
        max_length=30,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "+44 20 1234 5678",
                "autocomplete": "tel",
                "inputmode": "tel",
            }
        ),
    )

    enquiry_type = forms.ChoiceField(
        label="This enquiry is about",
        choices=ContactEnquiry.EnquiryType.choices,
        initial=ContactEnquiry.EnquiryType.GENERAL,
    )

    message = forms.CharField(
        label="Message",
        max_length=5000,
        widget=forms.Textarea(
            attrs={
                "placeholder": (
                    "Tell us about your property, your travel plans, "
                    "or what you would like to discuss..."
                ),
                "rows": 6,
            }
        ),
    )

    property_id = forms.UUIDField(
        required=False,
        widget=forms.HiddenInput,
    )

    # Honeypot field. Genuine visitors should leave this empty.
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "tabindex": "-1",
                "autocomplete": "off",
                "aria-hidden": "true",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        """Configure accessibility attributes for bound and unbound forms."""
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name in {"website", "property_id"}:
                continue

            error_id = f"{self[field_name].id_for_label}-error"

            if field_name == "phone":
                help_id = f"{self[field_name].id_for_label}-help"
                field.widget.attrs["aria-describedby"] = (
                    f"{help_id} {error_id}"
                )
            else:
                field.widget.attrs["aria-describedby"] = error_id

            if self.is_bound and self[field_name].errors:
                field.widget.attrs["aria-invalid"] = "true"

    def clean_name(self):
        """Normalise and validate the visitor's name."""
        name = self.cleaned_data["name"].strip()

        if len(name) < 2:
            raise forms.ValidationError(
                "Please enter your full name."
            )

        return name

    def clean_email(self):
        """Normalise the visitor's email address."""
        return self.cleaned_data["email"].strip().lower()

    def clean_phone(self):
        """Validate an optional telephone number in international format."""
        phone = self.cleaned_data.get("phone", "").strip()

        if not phone:
            return ""

        phone = re.sub(r"\s+", " ", phone)

        if not re.fullmatch(
            r"\+[1-9][\d\s().-]*",
            phone,
        ):
            raise forms.ValidationError(
                "Please enter an international telephone number beginning "
                "with its country code, for example +39 or +44."
            )

        digits = re.sub(r"\D", "", phone)

        if not 7 <= len(digits) <= 15:
            raise forms.ValidationError(
                "Please enter a valid international telephone number "
                "containing between 7 and 15 digits."
            )

        return phone

    def clean_message(self):
        """Reject empty or unhelpfully short messages."""
        message = self.cleaned_data["message"].strip()

        if len(message) < 10:
            raise forms.ValidationError(
                "Please provide a little more detail so we can help."
            )

        return message

    def clean_website(self):
        """Reject submissions that complete the honeypot field."""
        website = self.cleaned_data.get("website", "").strip()

        if website:
            raise forms.ValidationError(
                "Your enquiry could not be submitted."
            )

        return website

    def clean_property_id(self):
        """Accept only an existing, published rental-property UUID."""
        property_id = self.cleaned_data.get("property_id")

        if not property_id:
            return None

        exists = Property.objects.filter(
            public_id=property_id,
            published=True,
            available_for_rental=True,
        ).exists()

        if not exists:
            raise forms.ValidationError(
                "This property is not available for private rental enquiries."
            )

        return property_id

    def get_property(self):
        """Return the related published rental property, when supplied."""
        property_id = self.cleaned_data.get("property_id")

        if not property_id:
            return None

        return (
            Property.objects
            .filter(
                public_id=property_id,
                published=True,
                available_for_rental=True,
            )
            .first()
        )