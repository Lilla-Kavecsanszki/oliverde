from django.core.exceptions import ValidationError
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from services.content import ENQUIRY_TYPES

from .forms import ContactForm
from .models import ContactEnquiry
from .test_helpers import site_test_settings
from .validators import MAX_IMAGE_UPLOAD_BYTES, validate_image_size


class FakeImage:
    def __init__(self, size):
        self.size = size


class ImageSizeValidatorTests(SimpleTestCase):
    def test_small_image_is_accepted(self):
        validate_image_size(FakeImage(2 * 1024 * 1024))

    def test_image_at_the_limit_is_accepted(self):
        validate_image_size(FakeImage(MAX_IMAGE_UPLOAD_BYTES))

    def test_oversized_image_is_rejected_with_a_helpful_message(self):
        with self.assertRaises(ValidationError) as caught:
            validate_image_size(FakeImage(12.5 * 1024 * 1024))

        message = caught.exception.messages[0]
        self.assertIn("12.5 MB", message)
        self.assertIn("maximum is 10 MB", message)

    def test_object_without_a_size_is_ignored(self):
        validate_image_size(object())


class ContactFormTests(SimpleTestCase):
    def test_phone_field_mentions_whatsapp(self):
        self.assertEqual(
            ContactForm().fields["phone"].label,
            "Phone / WhatsApp",
        )

    def test_every_service_enquiry_type_is_a_valid_choice(self):
        valid = {value for value, _ in ContactEnquiry.EnquiryType.choices}

        for slug, enquiry_type in ENQUIRY_TYPES.items():
            self.assertIn(enquiry_type, valid, slug)


@site_test_settings
class ContactPreselectTests(TestCase):
    def selected_type(self, query):
        response = self.client.get(reverse("contact") + query)
        self.assertEqual(response.status_code, 200)
        return response.context["form"].initial.get("enquiry_type")

    def test_known_service_preselects_its_enquiry_type(self):
        self.assertEqual(
            self.selected_type("?service=restoration-management"),
            "restoration",
        )
        self.assertEqual(
            self.selected_type("?service=post-purchase-set-up"),
            "post_purchase",
        )

    def test_unknown_service_is_ignored(self):
        self.assertNotIn(
            self.selected_type("?service=does-not-exist"),
            set(ENQUIRY_TYPES.values()),
        )


@site_test_settings
class SitePageTests(TestCase):
    def test_main_pages_render(self):
        for name in ("home", "about", "contact"):
            with self.subTest(page=name):
                self.assertEqual(
                    self.client.get(reverse(name)).status_code,
                    200,
                )

    def test_services_come_before_portfolio_in_the_menu(self):
        html = self.client.get(reverse("home")).content.decode()
        nav = html[html.index("<header"):html.index("</header>")]

        self.assertLess(
            nav.index('href="/services/"'),
            nav.index('href="/portfolio/"'),
        )

    def test_stats_banner_is_identical_on_home_and_about(self):
        def stats(name):
            html = self.client.get(reverse(name)).content.decode()
            start = html.index('<section class="stats">')
            return html[start:html.index("</section>", start)]

        self.assertEqual(stats("home"), stats("about"))
        self.assertIn("since 2009", stats("about"))

    def test_founding_year_is_consistent(self):
        for name in ("home", "about"):
            html = self.client.get(reverse(name)).content.decode()
            self.assertIn("2009", html)
            self.assertNotIn("2006", html)

    def test_whatsapp_link_is_in_the_footer_and_contact_page(self):
        for name in ("home", "contact"):
            html = self.client.get(reverse(name)).content.decode()
            self.assertIn("https://wa.me/393663174740", html)

    def test_every_call_to_action_uses_the_same_background(self):
        for name in ("home", "about", "services:list", "portfolio:list"):
            with self.subTest(page=name):
                html = self.client.get(reverse(name)).content.decode()

                self.assertEqual(html.count("cta-background-image"), 1)
                self.assertIn("cta_oaimgv.jpg", html)

    def test_home_hero_is_served_from_cloudinary_and_preloaded(self):
        html = self.client.get(reverse("home")).content.decode()

        self.assertEqual(html.count("hero_vnkz5u.jpg"), 12)  # preload + image, 6 each
        self.assertIn('rel="preload"', html)
        self.assertIn("f_auto,q_auto", html)
        self.assertNotIn("images/tester.jpeg", html)

    def test_home_scroll_cue_links_to_the_next_section(self):
        html = self.client.get(reverse("home")).content.decode()

        self.assertIn('href="#after-hero"', html)
        self.assertIn('id="after-hero"', html)

    def test_spacing_stylesheet_loads_last(self):
        html = self.client.get(reverse("home")).content.decode()

        self.assertIn("css/spacing.css", html)
        self.assertGreater(
            html.index("css/spacing.css"),
            html.index("css/service-pages.css"),
        )

    def test_about_page_describes_the_team(self):
        html = self.client.get(reverse("about")).content.decode()

        self.assertIn("Oliver Beresford Manussis", html)
        self.assertIn("team of three", html)
        self.assertIn("accountant", html)
