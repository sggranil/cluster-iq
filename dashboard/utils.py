from urllib.parse import urlencode

from django.template.defaulttags import register
from django.urls import reverse


def chart_count_formatter(labels, counts):
    result = []

    for label, count in zip(labels, counts):
        result.append({
            "label": label,
            "count": count
        })

    return result


def reverse_url(view_name, *args, **kwargs):
    url = reverse(view_name, args=args)
    if not args:
        url = reverse(view_name)

    if kwargs:
        return f'{url}?{urlencode(kwargs)}'
    return url


@register.simple_tag
def url_with_params(view_name, *args, query=None):
    kwargs = {}
    if query.get('month'):
        kwargs['month'] = query['month']
    if query.get('barangay'):
        kwargs['barangay'] = query['barangay']

    return reverse_url(view_name, *args, **kwargs)
