import django.template.response

import consumer.models
import geographical.models
import geographical.utils

from django.contrib import messages


def index(request):
    template_path = 'pages/geographical.page.html'

    query = request.GET
    date = query.get('month', '').split('-')
    barangay = query.get('barangay')

    if len(date) != 2:
        return messages.error(request,"Invalid date format. Expected format: YYYY-MM.")

    datasets = consumer.models.ConsumerProfile.objects.filter(
        timestamp__month=int(date[0]), timestamp__year=int(date[1])
    )

    # if barangay:
    #     datasets = datasets.filter(barangay__name=barangay)

    average_income_per_barangay = geographical.utils.get_average_income_by_barangay(datasets, 5)
    average_spent_per_barangay = geographical.utils.get_average_spent_by_barangay(datasets, 5)
    most_demand_product = geographical.utils.get_most_demand_product_category(datasets, 5)
    top_demanded_product_per_barangay = geographical.utils.get_top_demanded_product_categories(datasets, 5)

    context = {
        'average_income_barangay': average_income_per_barangay,
        'average_spent_barangay': average_spent_per_barangay,
        'most_demand_product': most_demand_product,
        'demand_per_barangay': top_demanded_product_per_barangay
    }

    return django.template.response.TemplateResponse(request, template_path, context=context)


