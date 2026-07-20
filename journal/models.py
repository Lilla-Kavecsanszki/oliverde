from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class JournalPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    excerpt = models.CharField(max_length=300, help_text="Short teaser shown on the Journal list page.")
    body = RichTextUploadingField()
    cover_image = models.ImageField(upload_to="journal/covers/")

    related_properties = models.ManyToManyField(
        "portfolio.Property", related_name="journal_posts", blank=True,
        help_text="Optional — link this post to specific properties (e.g. a property spotlight)."
    )

    published_at = models.DateTimeField()
    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at"]

    def get_absolute_url(self):
        return reverse("journal:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title