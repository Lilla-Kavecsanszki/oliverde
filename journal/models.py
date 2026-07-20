from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field


class JournalPost(models.Model):
    title = models.CharField(max_length=200)

    slug = models.SlugField(
        unique=True,
        help_text="URL-friendly version of the title.",
    )

    excerpt = models.CharField(
        max_length=300,
        help_text="Short teaser shown on the Journal list page.",
    )

    body = CKEditor5Field(
        config_name="default",
    )

    cover_image = models.ImageField(
        upload_to="journal/covers/",
    )

    related_properties = models.ManyToManyField(
        "portfolio.Property",
        related_name="journal_posts",
        blank=True,
        help_text="Optional — link this post to one or more related properties.",
    )

    published_at = models.DateTimeField()

    is_published = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-published_at"]
        verbose_name = "Journal post"
        verbose_name_plural = "Journal posts"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "journal:detail",
            kwargs={"slug": self.slug},
        )