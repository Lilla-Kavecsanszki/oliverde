from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Your full name"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "your@email.com"})
    )
    phone = forms.CharField(
        max_length=30, required=False,
        widget=forms.TextInput(attrs={"placeholder": "+44 20 1234 5678"})
    )
    property_interest = forms.ChoiceField(
        required=False,
        choices=[
            ("", "General enquiry"),
            ("management", "Property management services"),
            ("rental", "Property rental / guest services"),
            ("other", "Something else"),
        ]
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Tell us about your property, or what you'd like to discuss...", "rows": 5})
    )