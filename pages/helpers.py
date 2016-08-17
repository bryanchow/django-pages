from .models import Page


def get_page(url):

    if not url.startswith("/"):
        url = "/" + url

    try:
        return Page.objects.get(url__exact=url)
    except Page.DoesNotExist:
        return None
