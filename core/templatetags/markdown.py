import markdown

from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter()
def md_as_html5(body):
    html = markdown.markdown(
        body, output_format='html5', extensions=['markdown.extensions.extra'])

    return mark_safe(html)
