from portfolio.models import Destination


def nav_destinations(request):
    """
    Makes the current list of Destinations available in every template's
    context as `nav_destinations`, so the Portfolio submenu in nav.html
    always reflects what's actually in the database — no template changes
    needed when destinations are added, renamed, or removed in admin.
    """
    return {"nav_destinations": Destination.objects.all()}
