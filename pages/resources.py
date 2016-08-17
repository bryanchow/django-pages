from django.conf import settings


DEFAULT_TEMPLATE = getattr(
    settings, 'DEFAULT_PAGE_TEMPLATE', "pages/default.html"
)

SITEMAP_CHANGEFREQ_CHOICES = [
    (1, 'always'),
    (2, 'hourly'),
    (3, 'daily'),
    (4, 'weekly'),
    (5, 'monthly'),
    (6, 'yearly'),
    (7, 'never'),
]

DEFAULT_SITEMAP_CHANGEFREQ = 3
