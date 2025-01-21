import django.template.response
import consumer.models
import re

from django.contrib import messages


def index(request):
    template_path = 'pages/dashboard.page.html'

    date = request.GET.get('month', '').split('-')
    if len(date) != 2:
        return messages.error(request,"Invalid date format. Expected format: YYYY-MM.")

    month = int(date[0])
    year = int(date[1])

    datasets = consumer.models.ConsumerProfile.objects.filter(
        timestamp__month=month, timestamp__year=year
    )

    total_respondents = datasets.count()
    spending_values = [extract_spending_value(record.income_level) for record in datasets if record.income_level]
    average_spending = sum(spending_values) / len(spending_values) if spending_values else 0
    weekly_purchase = datasets.filter(shopping_frequency="Weekly").count()

    context = {
        "analytics": {
            "total_respondents": total_respondents,
            "average_spending": f"₱{average_spending:,.0f}",
            "weekly_purchase": weekly_purchase,
        }
    }

    return django.template.response.TemplateResponse(request, template_path, context=context)


def extract_spending_value(income_range):
    match = re.match(r'₱([\d,]+)\s*-\s*₱([\d,]+)', income_range)
    if match:
        return float(match.group(1).replace(',', ''))

    return 0.0
