from django.conf import settings
from portfolio.models import Destination, Service


def nav_destinations(request):
    """
    Makes the current list of Destinations and Services available to every
    template so the Portfolio and Services navigation menus always reflect
    the current database content.
    """
    return {
        "nav_destinations": Destination.objects.all(),
        "nav_services": Service.objects.all(),
    }


def site_url(request):
    """
    Makes the site's canonical base URL available to every template.

    Used for:
    - Canonical URLs
    - Open Graph tags
    - Twitter/X Cards
    - robots.txt sitemap reference
    - sitemap.xml (if required)

    Update SITE_URL in settings.py when deploying to production.
    """
    return {
        "site_url": settings.SITE_URL,
    }