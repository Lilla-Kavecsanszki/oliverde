from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from core.test_helpers import (
    make_destination,
    make_property,
    make_service,
    site_test_settings,
)

from .models import Property

OWNER_CTA = "Would you like us to look after your home"


class PropertyPrivacyTests(TestCase):
    def test_internal_name_is_hidden_by_default(self):
        prop = make_property(public_title="Olive Grove House")

        self.assertEqual(prop.display_title, "Olive Grove House")
        self.assertNotEqual(prop.display_title, prop.title)

    def test_generic_title_is_used_when_no_public_title_is_set(self):
        prop = make_property()

        self.assertEqual(prop.display_title, "Private Farmhouse")

    def test_real_name_shows_only_when_approved(self):
        prop = make_property(show_real_name_publicly=True)

        self.assertEqual(prop.display_title, "Internal Farmhouse Name")

    def test_url_does_not_contain_the_internal_name(self):
        prop = make_property(public_title="Olive Grove House")

        self.assertNotIn("internal", prop.get_absolute_url().lower())
        self.assertIn(str(prop.public_id), prop.get_absolute_url())


class PropertyValidationTests(TestCase):
    def test_heated_pool_requires_a_pool(self):
        prop = make_property(pool=Property.PoolType.NONE, pool_heated=True)

        with self.assertRaises(ValidationError):
            prop.clean()

    def test_placeholder_style_details_need_a_matching_option(self):
        prop = make_property(
            air_conditioning=Property.AirConditioning.NONE,
            air_conditioning_details="ac details if any",
        )

        with self.assertRaises(ValidationError):
            prop.clean()

    def test_pool_details_need_a_pool(self):
        prop = make_property(
            pool=Property.PoolType.NONE,
            pool_details="Open May to October",
        )

        with self.assertRaises(ValidationError):
            prop.clean()

    def test_valid_property_passes(self):
        prop = make_property(
            pool=Property.PoolType.PRIVATE,
            pool_heated=True,
            pool_details="Heated, available from 1 May to 31 October.",
        )

        prop.clean()

    def test_rental_banner_only_when_available_for_rental(self):
        not_rental = make_property()
        rental = make_property(
            slug="rental-house",
            available_for_rental=True,
            rental_banner_text="",
        )

        self.assertEqual(not_rental.display_rental_banner, "")
        self.assertEqual(
            rental.display_rental_banner,
            "Available for Private Rental",
        )


@site_test_settings
class PortfolioPageTests(TestCase):
    def setUp(self):
        self.destination = make_destination()
        self.service = make_service()
        self.property = make_property(
            destination=self.destination,
            public_title="Olive Grove House",
        )
        self.property.services.add(self.service)

    def get_html(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, url)
        return response.content.decode()

    def test_every_portfolio_page_has_the_owner_call_to_action(self):
        urls = [
            reverse("portfolio:list"),
            reverse("portfolio:all_properties"),
            reverse("portfolio:holiday_rentals"),
            self.property.get_absolute_url(),
        ]

        for url in urls:
            with self.subTest(url=url):
                self.assertIn(OWNER_CTA, self.get_html(url))

    def test_call_to_action_background_is_shared_on_every_page(self):
        urls = [
            reverse("portfolio:all_properties"),
            self.destination.get_absolute_url(),
            self.property.get_absolute_url(),
        ]

        for url in urls:
            with self.subTest(url=url):
                html = self.get_html(url)

                self.assertEqual(html.count("cta-background-image"), 1)
                self.assertIn("cta_oaimgv.jpg", html)

    def test_call_to_action_mentions_optional_rental_management(self):
        html = self.get_html(reverse("portfolio:list"))

        self.assertIn("manage rentals and", html)

    def test_destination_page_speaks_to_owners_not_buyers(self):
        html = self.get_html(self.destination.get_absolute_url())

        self.assertIn("Own a home in Cortona?", html)
        self.assertNotIn("Looking for a home in", html)

    def test_property_page_never_shows_the_internal_name(self):
        html = self.get_html(self.property.get_absolute_url())

        self.assertIn("Olive Grove House", html)
        self.assertNotIn("Internal Farmhouse Name", html)

    def test_property_page_lists_how_we_look_after_homes(self):
        html = self.get_html(self.property.get_absolute_url())

        self.assertIn("How we look after homes like this one", html)
        self.assertIn(self.service.title, html)

    def test_enquire_button_appears_only_for_rental_homes(self):
        html = self.get_html(self.property.get_absolute_url())
        self.assertNotIn("Enquire About Staying", html)

        self.property.available_for_rental = True
        self.property.save()

        html = self.get_html(self.property.get_absolute_url())
        self.assertIn("Enquire About Staying", html)

    def test_unpublished_property_is_not_listed(self):
        self.property.published = False
        self.property.save()

        html = self.get_html(reverse("portfolio:all_properties"))

        self.assertNotIn("Olive Grove House", html)

    def test_unpublished_property_page_returns_404(self):
        self.property.published = False
        self.property.save()

        response = self.client.get(self.property.get_absolute_url())

        self.assertEqual(response.status_code, 404)

    def test_empty_results_use_a_button_that_is_visible_on_light_background(self):
        # The white "outline" button is only for dark bands; on the cream
        # empty-state background it would be invisible.
        self.property.published = False
        self.property.save()

        for name in ("portfolio:all_properties", "portfolio:holiday_rentals"):
            with self.subTest(page=name):
                html = self.get_html(reverse(name))
                start = html.index('class="empty-properties"')
                block = html[start:start + 900]

                self.assertIn("btn btn-primary", block)
                self.assertNotIn("btn-outline", block)

    def test_holiday_rentals_lists_only_rental_homes(self):
        make_property(
            slug="rental-house",
            public_title="Rental House",
            available_for_rental=True,
            destination=self.destination,
        )

        html = self.get_html(reverse("portfolio:holiday_rentals"))

        self.assertIn("Rental House", html)
        self.assertNotIn("Olive Grove House", html)
