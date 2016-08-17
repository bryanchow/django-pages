from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from . import resources
from .models import Page, Redirect


def page_view(request, url):

    if not url.startswith("/"):
        url = "/" + url

    try:
        page = Page.objects.get(url__exact=url)
        if page.template_name:
            template = loader.select_template(
                (page.template_name, resources.DEFAULT_TEMPLATE)
            )
        else:
            template = loader.get_template(resources.DEFAULT_TEMPLATE)
        return HttpResponse(template.render(RequestContext(request, {
            'page': page,
            'section': page.section,
        })))

    except Page.DoesNotExist:

        try:
            page = Redirect.objects.get(old_url__exact=url)
            return HttpResponseRedirect(page.new_url)

        except Redirect.DoesNotExist:
            if url.endswith("/") or not settings.APPEND_SLASH:
                raise Http404
            else:
                return HttpResponseRedirect("%s/" % url)
