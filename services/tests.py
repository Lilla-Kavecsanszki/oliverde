import re
from datetime import timedelta

from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.utils import timezone

from core.test_helpers import make_property, make_service, site_test_settings
from journal.models import JournalPost
from portfolio.models import Service, ServiceImage

from .content import COMMON_FAQS, ENQUIRY_TYPES, SERVICE_CONTENT


class ServiceContentTests(SimpleTestCase):
    def test_every_service_has_complete_content(self):
        for slug, content in SERVICE_CONTENT.items():
            with self.subTest(service=slug):
                self.assertTrue(content["overview"])
                self.assertTrue(content["who_for"])
                self.assertEqual(len(content["steps"]), 4)
                for step in content["steps"]:
                    self.assertTrue(step["title"])
                    self.assertTrue(step["text"])

    def test_enquiry_types_belong_to_known_services(self):
        self.assertTrue(set(ENQUIRY_TYPES) <= set(SERVICE_CONTENT))

    def test_copy_uses_british_spelling(self):
        text = repr(SERVICE_CONTENT) + repr(COMMON_FAQS)

        for american in ("personalized", "organized", "customized", "color"):
            self.assertNotIn(american, text.lower())

    def test_faqs_cover_informing_the_owner_and_privacy(self):
        questions = [faq["question"] for faq in COMMON_FAQS]

        self.assertIn("How will I stay informed about my property?", questions)
        self.assertIn("Is my dashboard private?", questions)


@site_test_settings
class ServiceListTests(TestCase):
    def setUp(self):
        self.service = make_service()

    def add_images(self, count):
        for index in range(count):
            ServiceImage.objects.create(
                service=self.service,
                image=f"services/gallery/{index}.jpg",
                caption=f"Caption {index}",
                order=index,
            )

    def get_html(self):
        response = self.client.get(reverse("services:list"))
        self.assertEqual(response.status_code, 200)
        return response.content.decode()

    def test_page_has_how_it_works_and_dashboard_sections(self):
        html = self.get_html()

        self.assertIn("How it works", html)
        self.assertIn("Your dashboard", html)

    def test_dashboard_section_describes_privacy_without_a_link(self):
        html = self.get_html()

        self.assertIn("private online dashboard", html)
        self.assertNotIn("drive.google.com", html)

    def test_no_gallery_without_images(self):
        html = self.get_html()

        self.assertNotIn("service-gallery-layout", html)

    def test_three_images_show_no_overflow_tile(self):
        self.add_images(3)
        html = self.get_html()

        self.assertEqual(html.count("<figure"), 3)
        self.assertNotIn('class="gallery-more"', html)

    def test_many_images_show_three_tiles_and_a_count(self):
        self.add_images(7)
        html = self.get_html()

        self.assertEqual(html.count("<figure"), 7)
        self.assertEqual(len(re.findall(r"^\s*hidden\s*$", html, re.M)), 4)
        self.assertIn("+4", html)
        self.assertIn("View all 7 photos", html)

    def test_gallery_combines_images_from_every_service(self):
        other = Service.objects.create(
            title="Property Rental",
            slug="property-rental",
            description="Guests.",
        )
        ServiceImage.objects.create(service=self.service, image="a.jpg")
        ServiceImage.objects.create(service=other, image="b.jpg")

        html = self.get_html()

        self.assertEqual(html.count("<figure"), 2)


@site_test_settings
class ServiceDetailTests(TestCase):
    def setUp(self):
        self.service = make_service()

    def get_html(self, slug=None):
        response = self.client.get(
            reverse("services:detail", kwargs={"slug": slug or self.service.slug})
        )
        self.assertEqual(response.status_code, 200)
        return response.content.decode()

    def test_every_service_with_content_renders_its_sections(self):
        for slug in SERVICE_CONTENT:
            Service.objects.get_or_create(
                slug=slug,
                defaults={
                    "title": slug.replace("-", " ").title(),
                    "description": "Description.",
                },
            )

            with self.subTest(service=slug):
                html = self.get_html(slug)

                self.assertIn("What to expect", html)
                self.assertIn("Good to know", html)
                self.assertIn("Every plan is tailored to your home", html)
                self.assertIn(f"?service={slug}", html)

    def test_service_without_content_still_renders(self):
        make_service(title="Concierge", slug="concierge")

        html = self.get_html("concierge")

        self.assertNotIn("What to expect", html)

    def test_unknown_service_returns_404(self):
        response = self.client.get(
            reverse("services:detail", kwargs={"slug": "nope"})
        )

        self.assertEqual(response.status_code, 404)

    def test_gallery_is_not_shown_on_service_pages(self):
        ServiceImage.objects.create(service=self.service, image="a.jpg")

        html = self.get_html()

        self.assertNotIn("service-gallery-layout", html)
        self.assertNotIn("property-lightbox", html)

    def test_properties_block_is_hidden_for_now(self):
        prop = make_property()
        prop.services.add(self.service)

        html = self.get_html()

        self.assertNotIn("Properties with this service", html)

    def test_only_published_listed_articles_are_shown(self):
        now = timezone.now()
        JournalPost.objects.create(
            title="Preparing a Tuscan home for winter",
            slug="preparing-tuscan-home-for-winter",
            excerpt="Winter care.",
            cover_image="journal/a.jpg",
            published_at=now - timedelta(days=1),
            is_published=True,
        )
        JournalPost.objects.create(
            title="Draft garden article",
            slug="care-tuscan-home-garden-summer",
            excerpt="Garden care.",
            cover_image="journal/b.jpg",
            published_at=now - timedelta(days=1),
            is_published=False,
        )

        html = self.get_html()

        self.assertIn("Preparing a Tuscan home for winter", html)
        self.assertNotIn("Draft garden article", html)
