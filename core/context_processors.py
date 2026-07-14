from portfolio.models import Destination, Service


def nav_destinations(request):
    """
    Makes the current list of Destinations and Services available in every
    template's context, so the Portfolio and Services submenus in nav.html
    always reflect what's actually in the database.
    """
    return {
        "nav_destinations": Destination.objects.all(),
        "nav_services": Service.objects.all(),
    }