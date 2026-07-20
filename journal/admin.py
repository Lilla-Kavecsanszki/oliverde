from django.contrib import admin
from .models import JournalPost


@admin.register(JournalPost)
class JournalPostAdmin(admin.ModelAdmin):
    list_display = ("title", "published_at", "is_published")
    list_filter = ("is_published",)
    search_fields = ("title", "excerpt", "body")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("related_properties",)
    date_hierarchy = "published_at"