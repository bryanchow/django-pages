from .helpers import get_page


def page(request):

    page = get_page(request.path)

    return {
        'page': page,
        'section': page.section if page else None,
    }
