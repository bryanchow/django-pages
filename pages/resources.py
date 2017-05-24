from collections import OrderedDict
from django.conf import settings


DEFAULT_TEMPLATE = getattr(
    settings, 'DEFAULT_PAGE_TEMPLATE', "pages/default.html"
)

SITEMAP_CHANGEFREQS = OrderedDict([
    (1, 'always'),
    (2, 'hourly'),
    (3, 'daily'),
    (4, 'weekly'),
    (5, 'monthly'),
    (6, 'yearly'),
    (7, 'never'),
])
SITEMAP_CHANGEFREQ_CHOICES = [
    (x, SITEMAP_CHANGEFREQS[x]) for x in SITEMAP_CHANGEFREQS
]

DEFAULT_SITEMAP_CHANGEFREQ = 3
