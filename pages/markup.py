from django.utils.safestring import mark_safe
from django.utils.html import linebreaks, escape
from django.contrib.markup.templatetags.markup import textile, markdown, restructuredtext


MARKUP_CHOICES = [
    ('plain', 'Plain text'),
    ('html', 'HTML'),
]

try:
    import textile as _textile
    MARKUP_CHOICES.append(('textile', 'Textile'))
except ImportError:
    pass

try:
    import markdown as _markdown
    MARKUP_CHOICES.append(('markdown', 'Markdown'))
except ImportError:
    pass

try:
    from docutils.core import publish_parts
    MARKUP_CHOICES.append(('rest', 'ReST'))
except ImportError:
    pass


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
