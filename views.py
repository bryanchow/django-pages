from datetime import datetime
from django.core.urlresolvers import get_resolver 
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from factorlib.pages.models import Page, Redirect


DEFAULT_TEMPLATE = 'pages/default.html'


def page(request, url):

    if not url.startswith('/'):
        url = "/" + url

    try:
        object = Page.on_site.get(url__exact=url)
        if object.template_name:
            template = loader.select_template((object.template_name, DEFAULT_TEMPLATE))
        else:
            template = loader.get_template(DEFAULT_TEMPLATE)
        return HttpResponse(template.render(RequestContext(request, {'page': object,})))

    except Page.DoesNotExist:

        try:
            object = Redirect.on_site.get(old_url__exact=url)
            return HttpResponseRedirect(object.new_url)

        except Redirect.DoesNotExist:
            if url.endswith('/') or not settings.APPEND_SLASH: 
                raise Http404 
            else:
                return HttpResponseRedirect('%s/' % url) 

