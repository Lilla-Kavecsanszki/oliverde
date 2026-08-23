from django import template
register = template.Library()

@register.filter
def optimize(url):
    if not url:
        return url
    return url.replace("/upload/", "/upload/f_auto,q_auto/")