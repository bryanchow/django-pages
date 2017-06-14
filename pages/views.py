from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from . import resources
from .models import Page, Redirect


def page_view(request, url):

    if not url.startswith("/"):
        url = "/" + url

    try:
        page = Page.objects.filter(url__exact=url)[0]
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

    except IndexError:
        try:
            page = Redirect.objects.filter(old_url__exact=url)[0]
            return HttpResponseRedirect(page.new_url)
        except IndexError:
            if url.endswith("/") or not settings.APPEND_SLASH:
                raise Http404
            else:
                return HttpResponseRedirect("%s/" % url)
