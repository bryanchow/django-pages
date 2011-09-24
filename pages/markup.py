from django.utils.safestring import mark_safe
from django.utils.html import linebreaks, escape
from django.contrib.markup.templatetags.markup import textile, markdown, restructuredtext


MARKUP_CHOICES = [
    ('plain',    'Plain text'),
    ('textile',  'Textile'),
    ('markdown', 'Markdown'),
    ('rest',     'ReST'),
    ('html',     'HTML'),
]


def render(source, markup):

    if markup == 'plain':
        return mark_safe(linebreaks(escape(source)))

    if markup == 'textile':
        return textile(source)

    if markup == 'markdown':
        return markdown(source)

    if markup == 'rest':
        return restructuredtext(source)

    if markup == 'html':
        return mark_safe(source)

    return None
