import re
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


def extract_spending_value(income_range):
    match = re.match(r'₱([\d,]+)\s*-\s*₱([\d,]+)', income_range)
    if match:
        return float(match.group(1).replace(',', ''))

    if income_range == 'Below ₱1,000':
        return 1000.0

    if income_range == '₱5,000 and above':
        return 5000.0

    return 0.0


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
    if 'consumer' in view_name:
        if query.get('age_group'):
            kwargs['age_group'] = query['age_group']
        if query.get('income_level'):
            kwargs['income_level'] = query['income_level']
        if query.get('barangay'):
            kwargs['barangay'] = query['barangay']

    return reverse_url(view_name, *args, **kwargs)
