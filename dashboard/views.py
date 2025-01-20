import django.template.response
import dashboard.utils


def index(request):
    template_path = 'pages/dashboard.page.html'
    age_group = dashboard.utils.chart_count_formatter(
        ['18 - 24 years old', '25 - 34 years old', '35 - 44 years old', '45 - 54 years old', '55+ years old'],
        [4, 6, 8, 10, 2]
    )
    monthly_spending = dashboard.utils.chart_count_formatter(
        ['₱0 - ₱999', '₱1,000 - ₱2,999', '₱3,000 - ₱4,999', '₱5,000+'],
        [9, 10, 5, 3]
    )
    shopping_frequency = dashboard.utils.chart_count_formatter(
        ['Weekly', 'Monthly', 'Less Often'],
        [9, 1, 2]
    )

    context = {
        "age_group": age_group,
        "monthly_spending": monthly_spending,
        "shopping_frequency": shopping_frequency
    }

    return django.template.response.TemplateResponse(request, template_path, context=context)
