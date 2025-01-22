import django.template.response
import consumer.models
import cluster_iq.utils
import consumer.utils
import re

from django.contrib import messages
from django.db.models import Count


def index(request):
    template_path = 'pages/dashboard.page.html'

    date = request.GET.get('month', '').split('-')

    if len(date) != 2:
        return consumer.utils.url_with_query_params(request,'dashboard:index', **{'month': '01-2025'})

    month = int(date[0])
    year = int(date[1])

    datasets = consumer.models.ConsumerProfile.objects.filter(
        timestamp__month=month, timestamp__year=year
    )

    # Analytics
    total_respondents = datasets.count()
    spending_values = [cluster_iq.utils.extract_spending_value(record.income_level) for record in datasets if record.income_level]
    average_spending = sum(spending_values) / len(spending_values) if spending_values else 0
    weekly_purchase = datasets.filter(shopping_frequency="Weekly").count()

    # Graph
    age_group_data = datasets.values('age_group').annotate(count=Count('age_group'))
    spending_category_data = datasets.values('spending_category').annotate(count=Count('spending_category'))
    shopping_frequency_data = datasets.values('shopping_frequency').annotate(count=Count('shopping_frequency'))

    age_group = cluster_iq.utils.chart_count_formatter(
        [entry['age_group'] for entry in age_group_data],
        [entry['count'] for entry in age_group_data]
    )
    monthly_spending = cluster_iq.utils.chart_count_formatter(
        [entry['spending_category'] for entry in spending_category_data],
        [entry['count'] for entry in spending_category_data]
    )
    shopping_frequency = cluster_iq.utils.chart_count_formatter(
        [entry['shopping_frequency'] for entry in shopping_frequency_data],
        [entry['count'] for entry in shopping_frequency_data]
    )

    context = {
        "analytics": {
            "total_respondents": total_respondents,
            "average_spending": f"₱{average_spending:,.0f}",
            "weekly_purchase": weekly_purchase,
        },
        "graph": {
            "age_group": age_group,
            "monthly_spending": monthly_spending,
            "shopping_frequency": shopping_frequency,
        }
    }

    return django.template.response.TemplateResponse(request, template_path, context=context)
