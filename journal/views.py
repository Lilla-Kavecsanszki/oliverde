from django.views.generic import ListView, DetailView
from .models import JournalPost


class JournalListView(ListView):
    model = JournalPost
    template_name = "journal/list.html"
    context_object_name = "posts"
    paginate_by = 9

    def get_queryset(self):
        return JournalPost.objects.filter(is_published=True)


class JournalDetailView(DetailView):
    model = JournalPost
    template_name = "journal/detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return JournalPost.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_properties"] = self.object.related_properties.filter(published=True)
        context["more_posts"] = JournalPost.objects.filter(
            is_published=True
        ).exclude(pk=self.object.pk)[:3]
        return context