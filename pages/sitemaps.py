from django.contrib.sitemaps import Sitemap
from factorlib.pages.models import Page


def get_visible_pages():
    return Page.objects.filter(visible=True)


class PageSitemap(Sitemap):

    def lastmod(self, obj):
        return obj.modified

    def changefreq(self, obj):
        return obj.sitemap_changefreq

    def priority(self, obj):
        return obj.sitemap_priority

    def items(self):
        return get_visible_pages()

